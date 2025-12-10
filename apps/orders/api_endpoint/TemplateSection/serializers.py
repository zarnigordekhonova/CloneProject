from rest_framework import serializers


class TemplateSectionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    order = serializers.IntegerField()
    width_mm = serializers.IntegerField()
    height_mm = serializers.IntegerField()