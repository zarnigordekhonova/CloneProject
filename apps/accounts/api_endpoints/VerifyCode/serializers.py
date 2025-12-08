from rest_framework import serializers


class VerifyCodeSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=14)
    code = serializers.CharField(max_length=6, min_length=6)

    def validate_code(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("Activation code must contain only digits.")
        return value
        








