from posts.views import post_list, post_detail, PostCreateView
from django.urls import path

urlpatterns = [

    path('', post_list, name="post_list"),
    path('<int:id>/', post_detail, name="post_detail"),
    path('create/', PostCreateView.as_view(), name='post_create'),

    # path('comment/',CommentCreateView.as_view(), name='comment_create'),


]