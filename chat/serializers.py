from rest_framework import serializers
from .models import Chat


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


    class Meta:
        model = Chat
        fields = ['id', 'title', 'content']


    def to_representation(self, obj):
        rep = super().to_representation(obj)
        rep['updated_at'] = obj.updated_at.strftime('%Y-%m-%d %H:%M')
        rep['writer_nickname'] = obj.writer.nickname
        rep['writer_profile_image'] = obj.writer.image.url
        return rep