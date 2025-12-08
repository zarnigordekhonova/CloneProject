from django.core.cache import cache
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from .serializers import VerifyCodeSerializer

User = get_user_model()


class VerifyCodeAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = VerifyCodeSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.data["phone_number"]
            code = serializer.data["code"]

            cache_key = f"verification_code_{phone_number}"
            stored_code = cache.get(cache_key)
            if stored_code is None:
                return Response(
                    {"error": "Verification code not found or expired"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            if code != stored_code:
                return Response(
                    {"error": "Invalid verification code"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            try:
                user = User.objects.get(phone_number=phone_number)
                user.is_active = True
                user.save()

                cache.delete(cache_key)

                from rest_framework_simplejwt.tokens import RefreshToken
                refresh_token = RefreshToken.for_user(user)

                return Response(
                    {"message": "Login successful",
                     "user_id" : user.id,
                     "phone_number": user.phone_number,
                     "full_name" : user.full_name,
                     "access_token": str(refresh_token.access_token),
                     "refresh_token": str(refresh_token)},
                     status=status.HTTP_200_OK
                )
            
            except User.DoesNotExist:
                return Response(
                    {"error" : "User not found"},
                    status=status.HTTP_404_NOT_FOUND
                )
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

__all__ = [
    "VerifyCodeAPIView"
]