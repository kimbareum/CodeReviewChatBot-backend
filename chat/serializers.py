from rest_framework import serializers
from .models import Chat
from datetime import datetime
import json


class ChatListSerializer(serializers.ModelSerializer):

    writer_nickname = serializers.SerializerMethodField()
    writer_profile_image = serializers.SerializerMethodField()

    class Meta:
        model = Chat
        fields = ['id', 'title', 'writer', 'view_count', 'created_at', 'updated_at', 'writer_nickname', 'writer_profile_image']

    def get_writer_nickname(self, obj):
        return obj.writer.nickname

    def get_writer_profile_image(self, obj):
        return obj.writer.image.url 
    
    def to_representation(self, obj):
        rep = super().to_representation(obj)
        rep['updated_at'] = obj.updated_at.strftime('%Y-%m-%d %H:%M')
        return rep


class ChatSerializer(serializers.ModelSerializer):

    title = serializers.CharField(required=False)
    content = serializers.CharField(required=False)

    class Meta:
        model = Chat
        fields = ['id', 'title', 'content']

    
    def validate(self, data):
        title = data.get('title')
        content = data.get('content')
        if not title:
            writer = self.context.get('request').user
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M')
            data['title'] = f"{writer}님의 {current_time} 질문"
        if content and not json.loads(content)[0].get('content'):
            raise serializers.ValidationError('질문은 필수 입력 값입니다.')

        return super().validate(data)


    def to_representation(self, obj):
        rep = super().to_representation(obj)
        rep['updated_at'] = obj.updated_at.strftime('%Y-%m-%d %H:%M')
        rep['writer_nickname'] = obj.writer.nickname
        rep['writer_profile_image'] = obj.writer.image.url
        return rep