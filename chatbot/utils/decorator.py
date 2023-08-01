from django.shortcuts import get_object_or_404
from django.http import Http404
from chat.models import Chat, Comment, ChildComment

def is_user_own(func):

    def wrapper(request, *args, **kwargs):
        post_id = kwargs.get('chat_id')
        comment_id = kwargs.get('comment_id')
        childcomment_id = kwargs.get('childcomment_id')
        if post_id:
            if request.user != get_object_or_404(Chat, pk=post_id).writer:
                raise Http404()
        kwargs.update({'user_owned': True})
        if comment_id:
            if request.user != get_object_or_404(Comment, pk=comment_id).writer:
                raise Http404()
        if childcomment_id:
            if request.user != get_object_or_404(ChildComment, pk=childcomment_id).writer:
                raise Http404()

        return func(request, *args, **kwargs)
    
    return wrapper