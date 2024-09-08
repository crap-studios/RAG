from rest_framework.serializers import ModelSerializer
from .models import Web3User


class Web3UserSerializer(ModelSerializer):
    class Meta:
        model = Web3User
        fields = ["id", "ethereum_address"]
