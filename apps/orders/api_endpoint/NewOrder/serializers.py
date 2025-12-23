from rest_framework import serializers

from apps.orders.models import NewOrder


class NewOrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = NewOrder
        fields = (
            "order_type",
            "company",
            "order_number",
            "quantity",
            "total_price",
            "cost_price",
            "profit",
            "discount_price",
            "advance_payment",
            "order_owner",
            "phone_number",
            "location",
            "additional_info"
        )

        read_only_fields = (
            "company",
            "total_price",
            "cost_price",
            "profit",
        )