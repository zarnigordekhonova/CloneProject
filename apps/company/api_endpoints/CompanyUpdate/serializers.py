from rest_framework import serializers

from apps.company.models import Company, ProductConfig
from apps.company.api_endpoints.CompanyAdd.serializers import CompanySerializer, ProductConfigSerializer


class CompanyProductConfigUpdateSerializer(serializers.Serializer):
    company = CompanySerializer(required=False)
    product_config = ProductConfigSerializer(many=True, required=False)

    def update(self, instance, validated_data):
        company_data = validated_data.pop("company", None)
        product_config_data = validated_data.pop("product_config", None)

        if company_data:
            for key, value in company_data.items():
                setattr(instance, key, value)
            instance.save()
        
        if product_config_data:
            for config in product_config_data:
                product_type = config.pop("product_type")

                ProductConfig.objects.update_or_create(
                    company=instance,
                    product_type=product_type,
                    defaults=config
                )
        return instance

    def to_representation(self, instance):
        return {
            "company": CompanySerializer(instance).data,
            "product_configs": ProductConfigSerializer(
                instance.product.all(),
                many=True
            ).data
        }