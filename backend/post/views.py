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
    def feed(self, request):
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
        txn = super().create(request, *args, **kwargs)

        raw_txn = self.contract.functions.addPrompt(
            request.data["prompt"], txn.data["id"]
        ).build_transaction(
            {
                "chainId": 696969,
                "gas": 2000000,
                "gasPrice": self.w3.to_wei("20", "gwei"),
                "nonce": self.w3.eth.get_transaction_count(
                    self.w3.to_checksum_address(web3_user.ethereum_address)
                ),
            }
        )

        return Response(
            {
                "message": "Image NFT created",
                "data": {
                    "image": txn.data,
                    "raw_txn": raw_txn,
                },
            },
            status=201,
        )

    @action(detail=True, methods=["POST"])
    def generate(self, request):
        signed_txn = request.data.get("signed_txn")
        image_id = request.data.get("image_id")

        if not image_id or not signed_txn:
            return Response({"message": "Invalid request"}, status=400)

        try:
            img_txn = ImagePromptTransaction.objects.get(id=image_id)
            img_txn.status = "processing"
            img_txn.save()
        except ImagePromptTransaction.DoesNotExist:
            return Response({"message": "Invalid transaction"}, status=400)

        txn_hash = self.w3.eth.send_raw_transaction(signed_txn)
        print(txn_hash)
        print(txn_hash.hex())

        return Response(
            {"message": "Image NFT generated"},
            status=200,
        )

    @action(detail=True, methods=["POST"])
    def mint(self, request):
        web3_user = Web3User.objects.get(user=request.user)
        image_id = request.data.get("image_id")
        txn = ImagePromptTransaction.objects.get(id=image_id)
        post = Post.objects.create(
            user=web3_user,
            content_type="image",
            token_id=txn.token_id,
            content=txn.response,
        )

        serializer = PostSerializer(post)

        return Response(
            {"message": "Image NFT minted", "data": serializer.data},
            status=201,
        )

    def retrieve(self, request, *args, **kwargs):
        img = super().retrieve(request, *args, **kwargs)

        return Response({"message": "Image NFT", "data": img.data}, status=200)
