from rest_framework import serializers

from apps.accounts.models import EmployeePayment
from apps.accounts.api_endpoints.EmployeeSalaryAdd.serializers import EmployeeSerializer


class EmployeeSalariesListSerializer(serializers.ModelSerializer):
    date = serializers.SerializerMethodField()

    class Meta:
        model = EmployeePayment
        fields = (
             "id",
             "employee",
             "amount",
             "date",
             )
        read_only_fields = ("id", "date",)


    def get_date(self, obj):
         return obj.created_at.date() if obj.created_at else None
    