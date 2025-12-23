from rest_framework import serializers

from apps.orders.models import OrderDetail, NewOrder, WindowOrder
from apps.orders.api_endpoint.NewOrder.serializers import NewOrderSerializer
from apps.orders.api_endpoint.WindowOrder.serializers import WindowOrderSerializer


class OrderDetailCreateSerializer(serializers.ModelSerializer):
    order = NewOrderSerializer(required=True)
    window_order = WindowOrderSerializer(required=True)

    class Meta:
        model = OrderDetail
        fields = (
            "order",
            "window_order",
            "material",
            "glass_layer",
            "glass_type",
            "provider",
            "include_waste_percentage",
            "waste_percentage",
            "profil_type",
            "has_balcony",
            "has_metal",
            "metal_thickness",
            "sash_profil_type",
            "frame_profile_type",
            "design_option",
            "design_variant",
            "shelf_width",
            "has_handle",
            "handle_type"
        )

    
    def create(self, validated_data):
        order_data = validated_data.pop("order")
        window_order_data = validated_data.pop("window_order")

        order = NewOrder.objects.create(**order_data)
        window_order = WindowOrderSerializer().create(window_order_data)

        order_detail = OrderDetail.objects.create(
            order=order,
            window_order=window_order,
            **validated_data
        )
        return order_detail
    
    # def to_representation(self, instance):
    #     data = super().to_representation(instance)
    #     if data["has_handle"] == True:

        
    



