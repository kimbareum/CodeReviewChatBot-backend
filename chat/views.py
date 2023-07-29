from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import permission_classes
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny

from .models import Chat
from .serializers import ChatListSerializer, ChatSerializer

from chatbot.utils.openAI_API import generate_response
from chatbot.utils.decorator import is_user_own

import json
# Create your views here.

User = get_user_model()


@permission_classes([AllowAny])
class ChatList(APIView):

    def get(self, request):
        page = int(request.GET.get('page', 0))
        chats = Chat.objects.prefetch_related('writer').all().order_by('-updated_at')

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

        context = {
        "chats": serialized_chats.data,
        "paginator": {
            "page_range": list(paginator.page_range),
            "current_page": page,
            },
        }

        return Response(context)


class UserChatList(APIView):

    def get(self, request):
        user = request.user
        if user:
            chats = Chat.objects.prefetch_related('writer').filter(writer=user).order_by('-updated_at')
            serialized_chats = ChatListSerializer(chats, many=True)

            return Response(serialized_chats.data)
        return Response('user가 존재하지 않습니다.')


@permission_classes([AllowAny])
class ChatDetail(APIView):

    def get(self, request, chat_id):
        try:
            chat = Chat.objects.prefetch_related('writer').get(pk=chat_id)
        except ObjectDoesNotExist as e:
            return Response(str(e), status=status.HTTP_404_NOT_FOUND)
        
        user = request.user
        user_owned = False
        if user and chat.writer == user:
            user_owned = True

        serialized_chat = ChatSerializer(chat)

        context = {
            "chat": serialized_chat.data,
            "user_owned": user_owned,
        }

        return Response(context)


class ChatWrite(APIView):

    def post(self, request):
        serializer = ChatSerializer(data=request.data, context={'request': request})
        # print(help(serializer.context))
        if serializer.is_valid():
            prompt = serializer.validated_data.get('content')
            response = generate_response(prompt)
            chat = serializer.save(writer=request.user, content=response)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @permission_classes([IsAuthenticated])
class ChatUpdate(APIView):

    # @method_decorator(ensure_csrf_cookie)
    # @method_decorator(csrf_protect)
    @method_decorator(is_user_own)
    def post(self, request, chat_id, user_owned):
        print(request.META)
        try:
            chat = Chat.objects.prefetch_related('writer').get(pk=chat_id)
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

    @method_decorator(is_user_own)
    def post(self, request, chat_id, user_owned):
        try:
            chat = Chat.objects.prefetch_related('writer').get(pk=chat_id)
        except ObjectDoesNotExist as e:
            return Response(str(e), status=status.HTTP_404_NOT_FOUND)
        chat.is_deleted = True
        chat.save()
        return Response("삭제되었습니다", status=status.HTTP_200_OK)