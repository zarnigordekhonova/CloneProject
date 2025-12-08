from rest_framework import serializers

from apps.accounts.models import Employee


class EmployeeListSerializer(serializers.ModelSerializer):
    created_date = serializers.SerializerMethodField()

    class Meta:
        model = Employee
        fields = (
            "id",
            "full_name",
            "created_date",
            "total_salary"
        )

    def get_created_date(self, obj):
        return obj.created_at.date() if obj.created_at else None