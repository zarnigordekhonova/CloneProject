from rest_framework import serializers

from apps.accounts.models import Employee, EmployeePayment


class EmployeeSerializer(serializers.ModelSerializer):
    created_date = serializers.SerializerMethodField()

    class Meta:
        model = Employee
        fields = (
            "id",
            "full_name",
            "total_salary",
            "created_date"
        )

    def get_created_date(self, obj):
            return obj.created_at.date() if obj.created_at else None


class EmployeeAddSalarySerializer(serializers.ModelSerializer):
    employee_data = EmployeeSerializer(source='employee', read_only=True)
    date = serializers.SerializerMethodField()

    class Meta:
        model = EmployeePayment
        fields = (
             "id",
             "employee",
             "amount",
             "date",
             "employee_data"
             )
        read_only_fields = ("id", "date", "employee_data", )


    def get_date(self, obj):
         return obj.created_at.date() if obj.created_at else None


