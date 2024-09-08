from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework_simplejwt.authentication import JWTAuthentication

from web3 import Web3
from eth_account.messages import encode_defunct

from django.contrib.auth.models import User
from django.contrib.auth import login
from .models import Web3User

from .serializers import Web3UserSerializer


# Create your views here.
class AuthViewSets(ModelViewSet):
    permission_classes = [AllowAny]

    @action(detail=False, methods=["GET"])
    def test(self, request):
        return Response({"message": "Hello World!"})

    @action(detail=False, methods=["POST"])
    def login(self, request):
        address = request.data.get("address")
        signature = request.data.get("signature")
        message = request.data.get("message")

        w3 = Web3()
        encoded_message = encode_defunct(text=message)
        recovered_address = w3.eth.account.recover_message(
            encoded_message, signature=signature
        )

        if recovered_address.lower() == address.lower():
            # Authentication successful
            user, _ = User.objects.get_or_create(username=address)
            web3_user, _ = Web3User.objects.get_or_create(
                user=user, ethereum_address=address
            )
            serialized_user = Web3UserSerializer(web3_user)
            refresh = RefreshToken.for_user(user)

            # # Get the new access token
            try:
                access_token = str(refresh.access_token)
            except TokenError:
                return Response(
                    {"detail": "Failed to generate access token."},
                    status=500,
                )

            return Response(
                {
                    "detail": "Logged in successfully.",
                    "data": {
                        "access_token": access_token,
                        "user": serialized_user.data,
                        "refresh_token": str(refresh),
                    },
                },
                status=200,
            )

        return Response(
            {
                "message": "Address verification failed. Please check your signature and try again."
            },
            status=400,
        )


class TokenRefreshViewSet(ModelViewSet):
    permission_classes = [AllowAny]

    def create(self, request):
        refresh_token = request.data.get("refresh_token")
        if not refresh_token:
            return Response(
                {"detail": "Refresh token is required."},
                status=400,
            )

        try:
            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)
            user_id = refresh.payload["user_id"]
            user = User.objects.get(id=user_id)
            web3user = Web3User.objects.get(user=user)
            serialized_user = Web3UserSerializer(web3user)

        except User.DoesNotExist:
            return Response(
                {"message": "Invalid refresh token."},
                status=400,
            )

        return Response(
            {"access_token": access_token, "user": serialized_user.data},
            status=200,
        )


class UserViewSets(ModelViewSet):
    queryset = Web3User.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self, request):
        user = request.user
        web3_user = Web3User.objects.get(user=user)
        serialized_users = Web3UserSerializer(web3_user)
        return Response(
            {"message": "User profile", "data": {"user": serialized_users.data}},
            status=200,
        )
