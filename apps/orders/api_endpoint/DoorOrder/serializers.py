from rest_framework import serializers

from apps.orders.models import DoorOrder, DoorOrderSection, Template
from apps.orders.api_endpoint.DoorOrderSections.serializers import DoorOrderSectionSerializer


class DoorOrderSerializer(serializers.ModelSerializer):
    sections = DoorOrderSectionSerializer(many=True, required=False)

    class Meta:
        model = DoorOrder
        fields = (
            "id", 
            "template",
            "width_mm",
            "height_mm",
            "total_price",
            "sections",
        )

        read_only_fields = ["total_price"]

    def create(self, validated_data):
        sections_data = validated_data.pop("sections", [])

        template = validated_data["template"]

        if template.template_type != Template.TemplateType.DOOR:
            raise serializers.ValidationError("Invalid template for Door order")

        template_sections = template.sections.all().order_by("section_order")
        template_sections_map = {s.section_order: s for s in template_sections}

        order = DoorOrder.objects.create(**validated_data)


        if sections_data:
            for sec in sections_data:
                tmp_section = template_sections_map.get(sec["section_order"])
 
                if tmp_section.orientation == "vertical":
                    width_mm = sec.get("width_mm", int(order.width_mm * tmp_section.width_ratio))
                    height_mm = sec.get("height_mm", order.height_mm)


                else:
                    width_mm = sec.get("width_mm", order.width_mm)
                    height_mm = sec.get("height_mm", int(order.height_mm * tmp_section.height_ratio))


                DoorOrderSection.objects.create(
                    order=order,
                    template_section=tmp_section,
                    section_order=sec["section_order"],
                    width_mm=width_mm,
                    height_mm=height_mm,
                )
        
        else:
            for tmp_sec in template_sections:

                if tmp_sec.orientation == "vertical":
                    width_mm = int(order.width_mm * tmp_sec.width_ratio) 
                    height_mm = int(order.height_mm * tmp_sec.height_ratio)
                else:  
                    width_mm = order.width_mm
                    height_mm = int(order.height_mm * tmp_sec.height_ratio)

                DoorOrderSection.objects.create(
                    order=order,
                    template_section=tmp_sec,
                    section_order=tmp_sec.section_order,
                    width_mm=width_mm,
                    height_mm=height_mm,
                )
        return order
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        base_price = instance.template.base_price_per_m2
        total_price = 0
        total_price = sum(sec.area_m2 * base_price for sec in instance.sections.all())

        data["total_price"] = total_price
        return data


