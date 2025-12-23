from rest_framework import serializers

from apps.orders.models import WindowOrder, WindowOrderSection, Template
from apps.orders.api_endpoint.WindowOrderSection.serializers import WindowOrderSectionSerializer


class WindowOrderSerializer(serializers.ModelSerializer):
    sections = WindowOrderSectionSerializer(many=True, required=False)

    class Meta:
        model = WindowOrder
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
        # print("VALIDATED DATA IN WINDOW ORDER SERIALIZER:", validated_data)
        # Foydalanuvchi shablon ichidagi qismlar razmerini o'zi belgilab ham jo'natishi mumkin
        sections_data = validated_data.pop("sections", [])

        template = validated_data["template"]

        if template.template_type != Template.TemplateType.WINDOW:
            raise serializers.ValidationError("Invalid template for Window order.")

        template_sections = template.sections.all().order_by("section_order")
        template_sections_map = {s.section_order: s for s in template_sections}

        order = WindowOrder.objects.create(**validated_data)
        
        # Agar foydalanuvchi shablon ichidagi qismlarni o'lchamini ham yuborgan bo'lsa, 
        # shu ma'lumotlar bo'yicha order yaratiladi
        
        # Agar u faqat shablonni umumiy o'lchamlarini yuborgan bo'lsa, unda ichki qismlar 
        # o'lchamlari database'dan olinadi, ya'ni default qiymatlar asosida order yaratiladi
        if sections_data:
            for sec in sections_data:
                tmp_section = template_sections_map.get(sec["section_order"])

                # Agar, ichki qism vertikal bo'lsa, unda foydalanuvchi, asosan, ichki qismlarni eni
                # o'lchamini yuborsa bo'ladi, bo'yi, shablondagi umumiy bo'yi o'lchami asosida ketaveradi 
                if tmp_section.orientation == "vertical":
                    width_mm = sec.get("width_mm", int(order.width_mm * tmp_section.width_ratio))
                    height_mm = sec.get("height_mm", order.height_mm)

                # Agar, ichki qism gorizontal tushgan bo'lsa, unda foydalanuvchi ichki qismlarni bo'yi
                # o'lchamini yuboradi, eni avtomatik ravishda, shablondagi umumiy eni o'lchami asosida bo'ladi
                else:
                    width_mm = sec.get("width_mm", order.width_mm)
                    height_mm = sec.get("height_mm", int(order.height_mm * tmp_section.height_ratio))


                WindowOrderSection.objects.create(
                    order=order,
                    template_section=tmp_section,
                    section_order=sec["section_order"],
                    width_mm=width_mm,
                    height_mm=height_mm,
                )
        
        # Agar, user ichki qismlar o'lchamlarini umuman yubormasa, ichki qismlar o'lchamlari, default holatda,
        # avvaldan belgilab qo'yilgan o'lchamlar bilan ketaveradi

        # Ichki qismlarni o'lchami ham admin panel orqali, shablonni umumiy o'lchamlari bilan birga beriladi.
        else:
            for tmp_sec in template_sections:

                if tmp_sec.orientation == "vertical":
                    width_mm = int(order.width_mm * tmp_sec.width_ratio) 
                    height_mm = int(order.height_mm * tmp_sec.height_ratio)
                else:  
                    width_mm = order.width_mm
                    height_mm = int(order.height_mm * tmp_sec.height_ratio)

                WindowOrderSection.objects.create(
                    order=order,
                    template_section=tmp_sec,
                    section_order=tmp_sec.section_order,
                    width_mm=width_mm,
                    height_mm=height_mm,
                )
        return order
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance.sections.exists():
            base_price = instance.template.base_price_per_m2
            total_price = sum(sec.area_m2 * base_price for sec in instance.sections.all())
            data["total_price"] = total_price
        else:
            data["total_price"] = float(instance.total_price)
        return data