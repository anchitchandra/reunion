from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView


from . import views


urlpatterns = [
    path('register/', views.RegisterUser.as_view(), name='register'),
    path('unfollow-follow/<int:id>/',  views.UnOrfollowUser.as_view(), name='unfollow_follow_user'),
    path('user/', views.GetUserDetails.as_view(), name='get_user'),
    path('posts/', views.CreatePost.as_view(), name='create_post'),
    path('posts/<int:id>/', views.RetriveORDeletePost.as_view(), name='get_or_delete_post'),
    path('like-unlike/<int:id>/', views.PostLikeUnlike.as_view(), name='likeUnlike_posts'),
    path('comment/<int:id>/', views.CommentOnPost.as_view(), name='comment_post'),
    path('all_posts/', views.GetCurrentUsersPost.as_view(), name='get_posts'),
]