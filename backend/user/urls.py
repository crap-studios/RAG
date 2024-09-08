from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import *

router = SimpleRouter()
router.register(r"auth", AuthViewSets, basename="auth")
router.register(r"refresh", TokenRefreshViewSet, basename="refresh-token")
router.register(r"user", UserViewSets, basename="user")


urlpatterns = [
    path("v1/", include(router.urls)),
]
