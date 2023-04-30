from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework.permissions import IsAuthenticated, AllowAny
from drf_yasg.utils import swagger_auto_schema

from .serializers import (
    CreateUserSerializer,
    UserSerializer,
    PostSerializer,
    CreateCommentSerializer,
)

from .models import User, Post




class RegisterUser(APIView):
    permission_classes = (AllowAny, )
    serializer_class = CreateUserSerializer
    @swagger_auto_schema(
        request_body=CreateUserSerializer
    )

    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)



class UnOrfollowUser(APIView):
    
    permission_classes = (IsAuthenticated,)

    def post(self,request, *args, **kwargs):
        id=kwargs.get("id", None)
        if id is None:
            return Response({'msg': 'Missing key Pair [id]'}, status=400)
        user = request.user
        user_to_unfollow = User.objects.filter(id=id)

        if not user_to_unfollow.exists():
            return Response({'msg': 'User not found'}, status=404)

        user_to_unfollowORfollow = user_to_unfollow.first()
        if user_to_unfollowORfollow == user:
            return Response({'msg': 'Method Not Allowed'}, status=400)
        
        if user_to_unfollowORfollow not in user.following.all():
            user.following.add(user_to_unfollowORfollow)
            user.save()
            return Response({"msg": f'User {user_to_unfollowORfollow.username} followed successfully'})
        
        if user_to_unfollowORfollow in user.following.all():
            user.following.remove(user_to_unfollowORfollow)
            user.save()
            return Response({"msg": f'User {user_to_unfollowORfollow.username} unfollowed successfully'})
        
        
        
        



class GetUserDetails(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self,request):
        user = request.user
        serializer = UserSerializer(user, many=False)
        return Response(serializer.data)

class CreatePost(APIView):

    permission_classes = (IsAuthenticated,)
    @swagger_auto_schema(
        request_body=PostSerializer
    )

    def post(self, request):
 
        serializer = PostSerializer(data=request.data)
        user = User.objects.get(email=request.user.email)
        if serializer.is_valid():
            serializer.save(user=user)
            return Response(serializer.data, status=201)
        return Response({"msg": serializer.errors}, status=400)


class RetriveORDeletePost(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self,request, *args, **kwargs):
        if not Post.objects.filter(id=kwargs.get("id", None)).exists():
            return Response({'msg': 'Post not found'}, status=404)
        post = post.first()

        serializer = PostSerializer(post, many=False)
        return Response(serializer.data)
    
    def delete(self,request, *args, **kwargs):
        if not Post.objects.filter(id=kwargs.get("id", None)).exists():
            return Response({'msg': 'Post not found'}, status=404)
        post = post.first()
        user = self.request.user.email
        if str(post.user) != str(user):
            return Response({'msg': 'Method Not Allowed'}, status=403)

        post_id = post.id
        post.delete()
        return Response({"msg": f'User {post.user}`s Post {post_id} deleted'})


class PostLikeUnlike(APIView):

    permission_classes = (IsAuthenticated,)

    def post(self,request, *args, **kwargs):
        user = self.request.user
        post = Post.objects.filter(id=kwargs.get("id", None))

        if not post.exists():
            return Response({'msg': 'Post not found'}, status=404)

        post = post.first()
        if post.user == user:
            return Response({'msg': 'Method not allowd'}, status=400)
        if post in user.liked_posts.all():
            user.liked_posts.remove(post)
            user.save()
            return Response({"msg": f'Post of {post.user} {post.id} unliked'}, status=200)
        if post not in user.liked_posts.all():
            user.liked_posts.add(post)
            user.save()
            return Response({"msg": f'Post of {post.user} {post.id} liked'}, status=200)
        
        
    
class CommentOnPost(APIView):

    permission_classes = (IsAuthenticated,)
    @swagger_auto_schema(
        request_body=CreateCommentSerializer
    )

    def post(self,request, *args, **kwargs):
        user = self.request.user
        post = Post.objects.filter(id=kwargs.get("id", None))

        if not post.exists():
            return Response({'msg': 'Not found'}, status=404)

        post = post.first()
        serializer = CreateCommentSerializer(data=self.request.data)

        if serializer.is_valid():
            comment = serializer.save(user=user, post=post)
            return Response({"commend_id": comment.id}, status=201)
        return Response({"msg": serializer.errors}, status=400)

class GetCurrentUsersPost(APIView):

    permission_classes = (IsAuthenticated,)
    def get(self,request):
        user = request.user
        posts = Post.objects.filter(user=user)
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status=200)
