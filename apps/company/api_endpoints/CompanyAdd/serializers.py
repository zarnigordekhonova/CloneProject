from rest_framework import serializers

from apps.company.models import Company, ProductConfig


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = (
            "id",
            "region",
            "district",
            "master",
            "dealer",
            "free_delivery",
            "telegram_link"
        )
        read_only_fields = ("id", "master",)


class ProductConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductConfig
        fields = (
            "id",
            "product_type",
            "is_in_percentage",
            "is_in_meter",
            "profit",
            "currency"
        )
        read_only_fields = ("id", )


class CompanyProductConfigSerializer(serializers.Serializer):
    company = CompanySerializer(required=True)
    product_config = ProductConfigSerializer(many=True, required=True)

    def create(self, validated_data):
        company_data = validated_data.pop("company")
        product_config_data = validated_data.pop("product_config")

        company = Company.objects.create(**company_data)

        for pro_conf in product_config_data:
            product = ProductConfig.objects.create (
                company=company,
                **pro_conf
            )

        return company
        
    def to_representation(self, instance):
        return {
            "company": CompanySerializer(instance).data,
            "product_config": ProductConfigSerializer(
                instance.product.all(),
                many=True
            ).data
        }

    
    
