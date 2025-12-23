from decimal import Decimal

from rest_framework import serializers

from apps.company.models import ProductConfig
from apps.orders.models import OrderDetail, NewOrder
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
            "material_type",
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

        company = self.context["request"].user.company.first()

        order = NewOrder.objects.create(
            company=company,
            **order_data
            )
        window_order = WindowOrderSerializer().create(window_order_data)

        order_detail = OrderDetail.objects.create(
            order=order,
            window_order=window_order,
            **validated_data
        )
        
        # calculation with master's profit values
        config = ProductConfig.objects.filter(
            company=company, 
            product_type=order_detail.material_type
        ).first()

        base_cost = window_order.total_price 
        profit_amount = Decimal("0.00")

        if config:
            # Percentage Profit
            if config.is_in_percentage:
                profit_amount = base_cost * (config.profit / Decimal("100"))

            # Per Meter Profit
            elif config.is_in_meter:
                width_m = Decimal(window_order.width) / Decimal("1000")
                height_m = Decimal(window_order.height) / Decimal("1000")
            
                area_m2 = width_m * height_m
                profit_amount = area_m2 * config.profit


        order.cost_price = base_cost           # window's base price
        order.profit = profit_amount           # master's profit value (ustaning qancha foyda olishi)
        order.total_price = base_cost + profit_amount  # overall price (buyurtmani umumiy narxi)
        order.save()
        return order_detail
    

        
    



