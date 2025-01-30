from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Blog, Comment
from .services import password_validate

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}
    
    def validate(self, data):
        # PASSWORD VALIDATION
        if not self.instance:
            result, detail = password_validate(data.get('password'))
            if not result:
                raise serializers.ValidationError({'detail': detail})                
        return data

    def create(self, validated_data):
        instance = User.objects.create(**validated_data)
        return instance
    
    def update(self, instance, validated_data):
        User.objects.filter(id = instance.id).update(**validated_data)
        instance = User.objects.filter(id = instance.id).first()
        return instance

class BlogSerializer(ModelSerializer):
    author = UserSerializer(read_only=True)
    likes_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Blog
        fields = ('id', 'title', 'content', 'author', 'created_at', 'likes_count', 'comments_count','is_active')

    def create(self, validated_data):
        instance = Blog.objects.create(**validated_data)
        return instance
    
    def update(self,  instance, validated_data):
        Blog.objects.filter(id=instance.id).update(**validated_data)
        instance =  Blog.objects.filter(id=instance.id).first()
        return instance

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_comments_count(self, obj):
        return obj.comments.count()

class CommentSerializer(ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'content', 'user', 'created_at')