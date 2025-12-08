from django.contrib.auth import get_user_model

from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveUpdateAPIView

from .serializers import UserGetUpdateProfileSerializer

User = get_user_model()


class UserGetUpdateProfileAPIView(RetrieveUpdateAPIView):
    serializer_class = UserGetUpdateProfileSerializer
    permission_classes = [IsAuthenticated, ]

    def get_object(self):
        return self.request.user
    


__all__ = [
    "UserGetUpdateProfileAPIView"
]

