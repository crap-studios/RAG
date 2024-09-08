from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import *

router = SimpleRouter()
router.register(r"post", PostViewSets, basename="post")
router.register(r"image", ImageNFTViewSets, basename="image-nft")


urlpatterns = [
    path("v1/", include(router.urls)),
]
