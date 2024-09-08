from django.db import models

from user.models import Web3User


# Create your models here.
class Post(models.Model):
    user = models.ForeignKey(Web3User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    content_type = models.CharField(
        max_length=10, choices=[("text", "Text"), ("image", "Image")]
    )
    content = models.TextField(blank=True, null=True)
    token_id = models.IntegerField(blank=True, null=True)


class ImagePromptTransaction(models.Model):
    id = models.UUIDField(primary_key=True, editable=False)
    user = models.ForeignKey(Web3User, on_delete=models.CASCADE)
    prompt = models.TextField(blank=False, null=False)
    status = models.CharField(
        max_length=10,
        choices=[
            ("created", "Created"),
            ("processing", "Processing"),
            ("processed", "Processed"),
        ],
        default="created",
    )
    response = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
