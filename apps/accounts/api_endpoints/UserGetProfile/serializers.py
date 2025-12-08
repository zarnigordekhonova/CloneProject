from django.contrib.auth import get_user_model

from rest_framework import serializers

User = get_user_model()


class UserGetUpdateProfileSerializer(serializers.ModelSerializer):
    country_name = serializers.CharField(source="country.name", read_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "full_name",
            "phone_number",
            "country",
            "country_name"
        )

        read_only_fields = (
            "id",
            "phone_number",
            "country",
            "country_name"
        )