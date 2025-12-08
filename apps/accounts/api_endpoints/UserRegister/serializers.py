from django.contrib.auth import get_user_model

from rest_framework import serializers

User = get_user_model()


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "country",
            "full_name",
            "phone_number"
        )

    def create(self, validated_data):
        user = User(
            country=validated_data.get("country"),
            full_name=validated_data.get("full_name"),
            phone_number=validated_data.get("phone_number"),
        )
        user.is_active = False  
        user.save()
        return user