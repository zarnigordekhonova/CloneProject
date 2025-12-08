from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.generics import CreateAPIView

from .serializers import UserRegisterSerializer

User = get_user_model()


class UserRegisterAPIView(CreateAPIView):
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny, ]



__all__ = [
    "UserRegisterAPIView",
]

