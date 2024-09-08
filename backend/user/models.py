from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Web3User(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ethereum_address = models.CharField(max_length=42, unique=True)
