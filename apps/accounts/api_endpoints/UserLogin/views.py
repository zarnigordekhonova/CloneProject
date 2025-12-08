from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import CustomTokenObtainPairSerializer

User  = get_user_model()


class UserLoginAPIView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    permission_classes = [AllowAny, ]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data.get("phone_number")
            print("VALIDATED_DATA: ", serializer.validated_data) 
            print("PHONE_NUMBER: ", phone_number)
            return Response(
                {"message": "Verification code has been sent", 
                 "phone_number": phone_number,
                 "expires_in": "10 minutes"},
                 status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


__all__ = [
    "UserLoginAPIView"
]



