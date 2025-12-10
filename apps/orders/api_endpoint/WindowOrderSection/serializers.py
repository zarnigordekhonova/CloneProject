from rest_framework import serializers

from apps.orders.models import WindowOrderSection


class WindowOrderSectionSerializer(serializers.ModelSerializer):
    area_m2 = serializers.FloatField(read_only=True)

    class Meta:
        model = WindowOrderSection
        fields = (
            "section_order",
            "template_section",
            "width_mm",
            "height_mm",
            "area_m2"
        )