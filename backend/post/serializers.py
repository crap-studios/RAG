from rest_framework import serializers
from .models import Post
from user.serializers import Web3UserSerializer


class PostSerializer(serializers.ModelSerializer):
    user = Web3UserSerializer(read_only=True)

    class Meta:
        model = Post
        fields = "__all__"


class ImagePromptTransactionSerializer(serializers.ModelSerializer):
    user = Web3UserSerializer(read_only=True)

    class Meta:
        model = Post
        fields = "__all__"
        read_only_fields = ["status", "response"]
