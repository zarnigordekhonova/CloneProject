from rest_framework import serializers

from apps.orders.models import DoorOrderSection


class DoorOrderSectionSerializer(serializers.ModelSerializer):
    area_m2 = serializers.FloatField(read_only=True)
    orientation = serializers.CharField(source="template_section.orientation", read_only=True)
    section_type = serializers.CharField(source="template_section.section_type", read_only=True)
    has_glass = serializers.BooleanField(source="template_section.has_glass", read_only=True)

    class Meta:
        model = DoorOrderSection
        fields = (
            "section_order",
            "template_section",
            "orientation",
            "section_type",
            "has_glass",
            "width_mm",
            "height_mm",
            "area_m2"
        )