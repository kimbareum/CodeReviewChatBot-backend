from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Chat, Comment, ChildComment
from datetime import datetime
import json


User = get_user_model()


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

    
    def validate(self, attrs):
        title = attrs.get('title')
        content = attrs.get('content')
        if not title:
            writer = self.context.get('request').user
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M')
            attrs['title'] = f"{writer}님의 {current_time} 질문"
        if content and not json.loads(content)[0].get('content'):
            raise serializers.ValidationError('질문은 필수 입력 값입니다.')

        return super().validate(attrs)


    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['updated_at'] = instance.updated_at.strftime('%Y-%m-%d %H:%M')
        rep['writer_nickname'] = instance.writer.nickname
        rep['writer_profile_image'] = instance.writer.image.url
        return rep


class ChildCommentSerializer(serializers.ModelSerializer):

    parent_comment_id = serializers.IntegerField()

    class Meta:
        model =ChildComment
        fields = ['id', 'content', 'parent_comment_id']

    def validate(self, attrs):
        content = attrs.get('content')
        parent_comment_id = attrs.get('parent_comment_id')

        try: 
            parent_comment = Comment.objects.get(pk=parent_comment_id)
            parent_comment.has_child = True
            parent_comment.save()
        except:
            raise ("존재하지 않는 댓글입니다.")
        
        return {"content": content, "parent_comment": parent_comment}


    def to_representation(self, instance):
        rep = super().to_representation(instance)
        if instance.is_deleted and instance.has_child:
            return None
        
        rep['created_at'] = instance.created_at.strftime('%Y-%m-%d %H:%M')
        rep['writer_nickname'] = instance.writer.nickname
        rep['writer_profile_image'] = instance.writer.image.url

        user = self.context['user']
        rep['user_owned'] = False
        if instance.writer == user:
            rep['user_owned'] = True
        return rep


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ['id', 'content']

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        user = self.context['user']
        if instance.is_deleted:
            rep['created_at'] = '--'
            rep['writer_nickname'] = '--'
            rep['writer_profile_image'] = '/media/anonymous.png'
            rep['user_owned'] = False
            rep['content'] = '삭제된 댓글입니다.'
            childComments = instance.child_comments.all()
            serializers = ChildCommentSerializer(childComments, many=True, context={'user':user})
            rep['child_comments'] = serializers.data
            return rep

        rep['created_at'] = instance.created_at.strftime('%Y-%m-%d %H:%M')
        rep['writer_nickname'] = instance.writer.nickname
        rep['writer_profile_image'] = instance.writer.image.url

        
        rep['user_owned'] = False
        if instance.writer == user:
            rep['user_owned'] = True
        if instance.has_child :
            childComments = instance.child_comments.all()
            serializers = ChildCommentSerializer(childComments, many=True, context={'user':user})
            rep['child_comments'] = serializers.data
        return rep


