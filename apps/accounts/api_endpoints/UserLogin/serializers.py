from django.core.cache import cache
from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from apps.accounts.utils import generate_activation_code

User = get_user_model()


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    phone_number = serializers.CharField(max_length=14)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if "username" in self.fields:
            del self.fields["username"]
        if "password" in self.fields:
            del self.fields["password"]


    def validate(self, attrs):
        phone_number = attrs.get("phone_number")

        try:
            user = User.objects.get(phone_number=phone_number)
        except User.DoesNotExist:
            raise serializers.ValidationError("User with this phone number does not exist")
        
        code = generate_activation_code()
        cache_key = f"verification_code_{phone_number}"
        cache.set(cache_key, code, timeout=600)

        print(f"\n VERIFICATION CODE for {phone_number}: {code}")
        print(f"Expires in 10 minutes\n")

        attrs['phone_number'] = phone_number

        return attrs
    
    def create(self, validated_data):
        pass

    @classmethod
    def get_token(cls, user):
        return super().get_token(user)
        
