from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Blog, Like, Comment
from .serializers import UserSerializer, BlogSerializer, CommentSerializer
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.tokens import RefreshToken
from .services import create_update_record

class UserViewSet(viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(methods=['post'], detail=False)
    def register(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            return Response(UserSerializer(instance).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(methods=['POST'], detail=False)
    def login(self, request):
        request_data = request.data.copy()
        user_data = User.objects.filter(username = request_data.get('username')).first()
        if user_data:
            # if check_password(request_data.get('password'), user_data.password):
            if request_data.get('password') == user_data.password:
                refresh = RefreshToken.for_user(user_data)
                access_token = str(refresh.access_token)
                refresh_token = str(refresh)
                serializer = UserSerializer(user_data)
                return Response({
                    "user": serializer.data,
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                }, status=status.HTTP_200_OK) 
            else:
                return Response({"error":"wrong password"},status=status.HTTP_400_BAD_REQUEST)   
        else:
            return Response({"error":"wrong username"},status=status.HTTP_400_BAD_REQUEST)   

class BlogViewSet(viewsets.GenericViewSet):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @action(methods=['GET','POST','PUT'], detail=False)
    def blog(self, request):
        if request.method == 'GET':
            queryset = Blog.objects.filter(is_active = True)
            serializer = BlogSerializer(queryset,many=True).data
            return Response(serializer,status=status.HTTP_200_OK)
        else:
            request_data = request.data
            return Response(create_update_record(request_data, Blog, BlogSerializer))

    @action(detail=False, methods=['post'])
    def like(self, request):
        blog = self.get_object()
        user = request.user
        like = Like.objects.filter(blog=blog, user=user).first()
        
        if like:
            like.delete()
            return Response({'status': 'unliked'}, status=status.HTTP_200_OK)
        
        Like.objects.create(blog=blog, user=user)
        return Response({'status': 'liked'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post','put'])
    def comment(self, request):
        request_data = request.data
        return Response(create_update_record(request_data, Comment, CommentSerializer))

    @action(detail=True, methods=['get'])
    def comments(self, request, pk=None):
        blog = self.get_object()
        comments = blog.comments.all()
        page = self.paginate_queryset(comments)
        serializer = CommentSerializer(page, many=True)
        
        paginated_response = self.get_paginated_response(serializer.data)
        paginated_response.data['page_number'] = self.paginator.page.number
        return paginated_response