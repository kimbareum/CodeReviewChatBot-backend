from django.shortcuts import redirect, get_object_or_404
from django.http import Http404
from django.contrib import messages
# from chat.models import Post, Comment

# def is_user_own(func):

#     def wrapper(request, *args, **kwargs):
#         post_id = kwargs.get('post_id')
#         comment_id = kwargs.get('comment_id')
#         if post_id:
#             if request.user != get_object_or_404(Post, pk=post_id).writer:
#                 raise Http404()
#         if comment_id:
#             if request.user != get_object_or_404(Comment, pk=comment_id).writer:
#                 raise Http404()

#         return func(request, *args, **kwargs)
    
#     return wrapper