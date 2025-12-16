from rest_framework import serializers

from apps.orders.models import NewOrder


class NewOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewOrder
        fields = (
            "order_type",
            "order_number",
            "quantity",
            "discount_price",
            "advance_payment",
            "order_owner",
            "phone_number",
            "location",
            "additional_info"
        )