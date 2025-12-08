from rest_framework import serializers

from apps.accounts.models import Employee


class CreateEmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = (
            "full_name",
            "phone_number",
            "profession",
            "share",
        )

        read_only_fields = (
            "id",
            "created_at"
        )

    def to_representation(self, instance):
        return {
            "Id": instance.id,
            "Full name" : instance.full_name,
            "Phone number" : instance.phone_number,
            "Profession" : instance.profession,
            "Share":  instance.share,
            "Created at" : instance.created_at
        }