from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import permission_classes
from rest_framework import status
from rest_framework.permissions import AllowAny

from .models import Chat, Comment, ChildComment
from .serializers import ChatListSerializer, ChatSerializer, CommentSerializer, ChildCommentSerializer
from chatbot.utils.openAI_API import generate_response
from chatbot.utils.decorator import is_user_own
from chatbot.utils.pages import get_page_data
from chatbot.utils.utils import get_visited_post

# Create your views here.

User = get_user_model()


@permission_classes([AllowAny])
class ChatList(APIView):

    throttle_scope = 'normal'

    def get(self, request):
        search_type = request.GET.get('type')
        search_text = request.GET.get('text')

        query = ''

        if search_type == 'title':
            query = Q(title__icontains=search_text)
        elif search_type == 'content':
            query = Q(content__icontains=search_text)
        elif search_type == 'writer':
            query = Q(writer__nickname__icontains=search_text)

        page = int(request.GET.get('page', 0))
        if query:
            chats = Chat.objects.select_related('writer').filter(query).order_by('-updated_at')
        else:
            chats = Chat.objects.select_related('writer').all().order_by('-updated_at')

        paginator = Paginator(chats, 10)

        try:
            page_object = paginator.page(page)
        except PageNotAnInteger:
            page = 1
            page_object = paginator.page(page)
        except EmptyPage:
            if page <= 0:
                page = 1
                page_object = paginator.page(page)
            else:
                page = paginator.num_pages
                page_object = paginator.page(page)

        serialized_chats = ChatListSerializer(page_object, many=True)

        page_data = get_page_data(page, len(paginator.page_range))

        context = {
        "chats": serialized_chats.data,
        "paginator": page_data,
        }

        return Response(context)


class UserChatList(APIView):

    throttle_scope = 'normal'

    def get(self, request):
        user = request.user
        if user:
            chats = Chat.objects.select_related('writer').filter(writer=user).order_by('-updated_at')
            serialized_chats = ChatListSerializer(chats, many=True)

            return Response(serialized_chats.data)
        return Response('user가 존재하지 않습니다.')


@permission_classes([AllowAny])
class ChatDetail(APIView):

    throttle_scope = 'normal'

    def get(self, request, chat_id):
        try:
            chat = Chat.objects.prefetch_related('writer', 'comment_set__child_comments').get(pk=chat_id)
        except ObjectDoesNotExist as e:
            return Response(str(e), status=status.HTTP_404_NOT_FOUND)

        user = request.user
        user_owned = False
        if user and chat.writer == user:
            user_owned = True

        visited_post = get_visited_post(request, chat_id)

        if visited_post.get('flag'):
            chat.view_count += 1
            chat.save(update_fields=['view_count'])
        serialized_chat = ChatSerializer(chat)
        serialized_comments = CommentSerializer(chat.comment_set.filter(Q(is_deleted=False) | (Q(is_deleted=True) & Q(child_count__gte=1))), many=True, context={"user":user})

        context = {
            "chat": serialized_chat.data,
            "comments": serialized_comments.data,
            "user_owned": user_owned,
            "visited_post": visited_post.get('value'),
        }

        return Response(context)


# @throttle_scope([UserRateThrottle])
class ChatWrite(APIView):

    throttle_scope = 'question'

    def post(self, request):
        serializer = ChatSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            prompt = serializer.validated_data.get('content')
            response = generate_response(prompt)
            chat = serializer.save(writer=request.user, content=response)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# @throttle_scope([UserRateThrottle])
class ChatUpdate(APIView):

    throttle_scope = 'question'

    @method_decorator(is_user_own)
    def post(self, request, chat_id, user_owned):

        try:
            chat = Chat.objects.select_related('writer').get(pk=chat_id)
        except ObjectDoesNotExist as e:
            return Response(str(e), status=status.HTTP_404_NOT_FOUND)
        serializer = ChatSerializer(chat, data=request.data)
        if serializer.is_valid():
            prompt = serializer.validated_data.get('content')
            if prompt:
                response = generate_response(prompt)
                serializer.validated_data['content'] = response
            serializer.save()
            context = {
                "chat": serializer.data,
                "user_owned": user_owned,
            }
            return Response(context, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChatDelete(APIView):

    throttle_scope = 'normal'

    @method_decorator(is_user_own)
    def post(self, request, chat_id, user_owned):
        try:
            chat = Chat.objects.get(pk=chat_id)
        except ObjectDoesNotExist as e:
            return Response(str(e), status=status.HTTP_404_NOT_FOUND)
        chat.is_deleted = True
        chat.save()
        return Response("삭제되었습니다", status=status.HTTP_200_OK)


### Comment
class CommentWrite(APIView):

    throttle_scope = 'normal'

    def post(self, request, chat_id):
        
        user = request.user

        chat = None
        
        if request.data.get('parent_comment_id'):
            serializer = ChildCommentSerializer(data=request.data)
        else:
            serializer = CommentSerializer(data=request.data)
            try:
                chat = Chat.objects.get(pk=chat_id)
            except ObjectDoesNotExist as e:
                return Response(str(e), status=status.HTTP_404_NOT_FOUND)

        if serializer.is_valid():
            user=request.user
            if chat:
                serializer.save(writer=user, chat=chat)
            else:
                serializer.save(writer=user)

            comments = Comment.objects.filter(chat=chat)
            serialized_comments = CommentSerializer(comments, many=True, context={"user":user})

            return Response(serialized_comments.data, status=status.HTTP_201_CREATED)
        
        return Response("error", status=status.HTTP_400_BAD_REQUEST)


class CommentUpdate(APIView):

    throttle_scope = 'normal'

    @method_decorator(is_user_own)
    def post(self, request, **kwargs):
        comment_id = kwargs.get('comment_id')
        childcomment_id = kwargs.get('childcomment_id')

        if comment_id:
            try:
                comment = Comment.objects.get(pk=comment_id)
            except ObjectDoesNotExist as e:
                return Response(str(e), status=status.HTTP_404_NOT_FOUND)
        if childcomment_id:
            try:
                comment = ChildComment.objects.get(pk=childcomment_id)
            except ObjectDoesNotExist as e:
                return Response(str(e), status=status.HTTP_404_NOT_FOUND)
        
        content = request.data.get('content')
        if content:
            comment.content = content
            comment.save()
            chat_id = comment.chat.pk
            try:
                comments = Comment.objects.prefetch_related('child_comments').filter(chat=chat_id)
            except ObjectDoesNotExist as e:
                return Response(str(e), status=status.HTTP_404_NOT_FOUND)
            serializer = CommentSerializer(comments, many=True, context={'user': request.user})
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response("error", status=status.HTTP_400_BAD_REQUEST)



class CommentDelete(APIView):

    throttle_scope = 'normal'

    @method_decorator(is_user_own)
    def post(self, request, **kwargs):
        comment_id = kwargs.get('comment_id')
        childcomment_id = kwargs.get('childcomment_id')
        if comment_id:
            try:
                comment = Comment.objects.get(pk=comment_id)
            except ObjectDoesNotExist as e:
                return Response(str(e), status=status.HTTP_404_NOT_FOUND)
        if childcomment_id:
            try:
                comment = ChildComment.objects.get(pk=childcomment_id)
                parent_comment = comment.parent_comment
                parent_comment.child_count -= 1
                parent_comment.save()
            except ObjectDoesNotExist as e:
                return Response(str(e), status=status.HTTP_404_NOT_FOUND)
            
        comment.is_deleted = True
        comment.save()
        chat_id = comment.chat.pk

        try:
            comments = Comment.objects.prefetch_related('child_comments').filter(chat=chat_id)
        except ObjectDoesNotExist as e:
            return Response(str(e), status=status.HTTP_404_NOT_FOUND)
        
        serializer = CommentSerializer(comments, many=True, context={'user': request.user})
        return Response(serializer.data, status=status.HTTP_200_OK)



