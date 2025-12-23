from decimal import Decimal 

from django.contrib import admin
from django.utils.html import format_html

from apps.company.models import Dealer, Company, ProductConfig, Provider 


class ProductConfigInline(admin.TabularInline):
    model = ProductConfig
    extra = 1
    
    fields = (
        "product_type", 
        "is_in_percentage", 
        "is_in_meter", 
        "profit", 
        "currency",
        "created_at",
    )
    
    readonly_fields = ("created_at",)


@admin.register(Dealer)
class DealerAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "created_at")
    search_fields = ("name",)
    readonly_fields = ("created_at", "updated_at")
    ordering = ("name",)


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    
    list_display = (
        "id",
        "master",
        "dealer_name", 
        "region_name", 
        "district_name", 
        "free_delivery", 
        "created_at"
    )
    
    list_filter = (
        "dealer", 
        "free_delivery",
        "region", 
        "district",
    )
    
    search_fields = (
        "dealer__name", 
        "region__name", 
        "district__name",
    )
    
    readonly_fields = ("created_at", "updated_at")
    
    fieldsets = (
        (None, {
            'fields': ("dealer", "master", "free_delivery", "telegram_link"),
        }),
        ('Location', {
            'fields': ("region", "district"),
        }),
        ('Timestamps', {
            'fields': ("created_at", "updated_at"),
            'classes': ('collapse',),
        })
    )
    
    inlines = [ProductConfigInline]
    

    @admin.display(description='Dealer Name')
    def dealer_name(self, obj):
        return obj.dealer.name
        
    @admin.display(description='Region')
    def region_name(self, obj):
        return obj.region.name
        
    @admin.display(description='District')
    def district_name(self, obj):
        return obj.district.name


@admin.register(ProductConfig)
class ProductConfigAdmin(admin.ModelAdmin):
    
    list_display = (
        "id",
        "company_dealer_name", 
        "product_type", 
        "profit", 
        "currency", 
        "is_in_percentage", 
        "is_in_meter",
    )
    
    list_filter = (
        "product_type",
        "is_in_percentage",
        "is_in_meter",
        "currency",
        "company__dealer", 
    )
    
    search_fields = (
        "company__dealer__name", 
        "product_type",
    )
    
    readonly_fields = ("created_at", "updated_at")
    ordering = ("company__dealer__name", "product_type")

    @admin.display(description='Company / Dealer')
    def company_dealer_name(self, obj):
        return obj.company.dealer.name


@admin.register(Provider)
class ProviderAdmin(admin.ModelAdmin):
    """Admin configuration for the Provider model."""
    list_display = ("name", "logo_thumbnail", "created_at")
    search_fields = ("name",)
    readonly_fields = ("created_at", "updated_at", "logo_thumbnail")
    ordering = ("name",)
    
    
    @admin.display(description='Logo Preview')
    def logo_thumbnail(self, obj):
        if obj.logo:
            # Adjust max_height to control thumbnail size
            return format_html('<img src="{}" style="max-height: 50px;" />', obj.logo.url)
        return "No Image"