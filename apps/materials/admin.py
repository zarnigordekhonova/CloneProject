from decimal import Decimal

from django.contrib import admin
from django.utils.html import format_html

from apps.materials.models import (
    DesignOption, DesignVariant, MaterialType, ProfilType,
    GlassLayer, GlassType, SashProfilType, FrameProfilType, 
    HandleType, Category, Product, CustomProduct
)


class DesignVariantInline(admin.TabularInline):
    model = DesignVariant
    extra = 1
    fields = ("name", "image", "image_thumbnail")
    readonly_fields = ("image_thumbnail",)
    
    @admin.display(description='Image Preview')
    def image_thumbnail(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 50px;" />', obj.image.url)
        return "No Image"

class ProfilTypeInline(admin.TabularInline):
    model = ProfilType
    extra = 1
    fields = ("name",)

class GlassTypeInline(admin.TabularInline):
    model = GlassType
    extra = 1
    fields = ("name", "price", "currency")
    raw_id_fields = ('currency',) 

@admin.register(DesignOption)
class DesignOptionAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "created_at")
    search_fields = ("name",)
    readonly_fields = ("created_at", "updated_at")
    inlines = [DesignVariantInline]


@admin.register(MaterialType)
class MaterialTypeAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "created_at")
    search_fields = ("name",)
    readonly_fields = ("created_at", "updated_at")
    inlines = [ProfilTypeInline]


@admin.register(GlassLayer)
class GlassLayerAdmin(admin.ModelAdmin):
    list_display = ("id", "layer", "created_at")
    search_fields = ("layer",)
    readonly_fields = ("created_at", "updated_at")
    inlines = [GlassTypeInline]

def get_image_thumbnail_display(obj):
    if obj.image:
        return format_html('<img src="{}" style="max-height: 50px; max-width: 50px;" />', obj.image.url)
    return "No Image"


@admin.register(SashProfilType)
class SashProfilTypeAdmin(admin.ModelAdmin):
    list_display = ("id", get_image_thumbnail_display, "created_at")
    readonly_fields = ("created_at", "updated_at", get_image_thumbnail_display)


@admin.register(FrameProfilType)
class FrameProfilTypeAdmin(admin.ModelAdmin):
    list_display = ("id", "name", get_image_thumbnail_display, "created_at")
    search_fields = ("name",)
    readonly_fields = ("created_at", "updated_at", get_image_thumbnail_display)


@admin.register(HandleType)
class HandleTypeAdmin(admin.ModelAdmin):
    list_display = ("id", get_image_thumbnail_display, "created_at")
    readonly_fields = ("created_at", "updated_at", get_image_thumbnail_display)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "created_at")
    search_fields = ("name",)
    readonly_fields = ("created_at", "updated_at")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name", 
        "provider", 
        "category", 
        "material", 
        "design", 
        "price", 
        "image_thumbnail"
    )
    
    list_filter = ("provider", "category", "material", "design")
    
    search_fields = (
        "name", 
        "provider__name", 
        "category__name", 
        "material__name"
    )
    
    readonly_fields = ("created_at", "updated_at", "image_thumbnail")
    
    @admin.display(description='Image Preview')
    def image_thumbnail(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 50px;" />', obj.image.url)
        return "No Image"


@admin.register(CustomProduct)
class CustomProductAdmin(admin.ModelAdmin):
    """Admin for the CustomProduct model."""
    list_display = (
        "id",
        "name", 
        "provider_name", 
        "category", 
        "measurement_unit",
        "ordinary_price",
        "colorful_price",
        "image_thumbnail"
    )
    
    list_filter = ("category", "measurement_unit")
    
    search_fields = ("name", "provider_name", "category__name")
    
    fieldsets = (
        (None, {
            'fields': ("name", "category", "provider_name", "image"),
        }),
        ('Pricing & Measurement', {
            'fields': (
                "measurement_unit", 
                "measurement_value", 
                "ordinary_price", 
                "colorful_price"
            ),
        }),
        ('Timestamps', {
            'fields': ("created_at", "updated_at"),
            'classes': ('collapse',),
        })
    )
    
    readonly_fields = ("created_at", "updated_at", "image_thumbnail")

    @admin.display(description='Image Preview')
    def image_thumbnail(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 50px;" />', obj.image.url)
        return "No Image"