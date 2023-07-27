from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import permission_classes
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny

from .models import Chat
from .serializers import ChatListSerializer, ChatSerializer

from chatbot.utils.openAI_API import generate_response
from chatbot.utils.jwt import get_user_from_jwt 

import json
# Create your views here.

User = get_user_model()


@permission_classes([AllowAny])
class ChatList(APIView):

    def get(self, request):
        chats = Chat.objects.prefetch_related('writer').all().order_by('-updated_at')
        serialized_chats = ChatListSerializer(chats, many=True)

        return Response(serialized_chats.data)


class UserChatList(APIView):

    def get(self, request):
        # token = request.COOKIES.get('access_token')
        # user = get_user_from_jwt(token)
        user = request.user
        if user:
            chats = Chat.objects.prefetch_related('writer').filter(writer=user).order_by('-updated_at')
            serialized_chats = ChatListSerializer(chats, many=True)

            return Response(serialized_chats.data)
        return Response('[{}]')


@permission_classes([AllowAny])
class ChatDetail(APIView):

    def get(self, request, chat_id):
        try:
            chat = Chat.objects.prefetch_related('writer').get(pk=chat_id)
        except ObjectDoesNotExist as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
        serialized_chat = ChatSerializer(chat)
        return Response(serialized_chat.data)


class ChatWrite(APIView):

    def post(self, request):
        serializer = ChatSerializer(data=request.data)
        if serializer.is_valid():
            prompt = serializer.validated_data.get('content')
            response = generate_response(prompt)
            serializer.save(writer=User.objects.get(pk=1), content=response)
            
        return Response(serializer.data)


class ChatUpdate(APIView):

    def post(self, request, chat_id):
        print(request.META)
        try:
            chat = Chat.objects.prefetch_related('writer').get(pk=chat_id)
        except ObjectDoesNotExist as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
        serializer = ChatSerializer(chat, data=request.data)
        if serializer.is_valid():
            prompt = serializer.validated_data.get('content')
            response = generate_response(prompt)
            chat.content = response
            chat.save()
            return Response(ChatSerializer(chat).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)