from web3 import Web3

from typing import Any
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from django.conf import settings

from user.models import Web3User
from .models import Post, ImagePromptTransaction
from .serializers import PostSerializer, ImagePromptTransactionSerializer
from .utils import get_contract_abi


class PostViewSets(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        web3user = Web3User.objects.get(user=self.request.user)
        serializer.save(user=web3user)

    def list(self, request):
        posts = Post.objects.filter(user__id=request.user.id)
        serializer = PostSerializer(posts, many=True)
        return Response({"message": "User posts", "data": serializer.data}, status=200)

    @action(detail=False, methods=["GET"])
    def following(self, request):
        web3_user = Web3User.objects.get(user=request.user)
        followers = web3_user.followers.all()
        follower_ids = [follower.id for follower in followers]
        posts = Post.objects.filter(user__id__in=follower_ids)
        serializer = PostSerializer(posts, many=True)
        return Response(
            {"message": "User following post", "data": serializer.data}, status=200
        )

    def create(self, request, *args, **kwargs):
        post = super().create(request, *args, **kwargs)

        return Response({"message": "Post created", "data": post.data}, status=201)


class ImageNFTViewSets(ModelViewSet):
    queryset = ImagePromptTransaction.objects.all()
    serializer_class = ImagePromptTransactionSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.w3 = Web3(Web3.HTTPProvider(settings.IMAGEGEN_RPC_URL))
        self.contract_abi = get_contract_abi(settings.IMAGEGEN_CONTRACT_NAME)
        self.contract = self.w3.eth.contract(
            address=settings.IMAGEGEN_CONTRACT_ADDRESS, abi=self.contract_abi
        )

    def perform_create(self, serializer):
        web3user = Web3User.objects.get(user=self.request.user)
        serializer.save(user=web3user, status="created")

    def create(self, request, *args, **kwargs):
        web3_user = Web3User.objects.get(user=request.user)
        # txn = super().create(request, *args, **kwargs)

        raw_txn = self.contract.functions.addPrompt(
            web3_user.ethereum_address, request.data["prompt"]
        ).buildTransaction(
            {
                "chainId": 6969,
                "gas": 2000000,
                "gasPrice": self.w3.toWei("20", "gwei"),
                "nonce": self.w3.eth.get_transaction_count(web3_user.ethereum_address),
            }
        )

        return Response(
            {
                "message": "Image NFT created",
                "data": {
                    # "image": txn,
                    "raw_txn": raw_txn,
                },
            },
            status=201,
        )
