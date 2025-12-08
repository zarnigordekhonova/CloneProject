from decimal import Decimal 
from django.contrib import admin

from apps.common.models import Country, Region, District, Currency


class DistrictInline(admin.TabularInline):
    model = District
    extra = 1 
    fields = ("name",)

class RegionInline(admin.TabularInline):
    model = Region
    extra = 1
    fields = ("name",)


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    """Admin configuration for the Country model."""
    list_display = ("id", "name", "code", "created_at", "updated_at")
    search_fields = ("name", "code")
    readonly_fields = ("created_at", "updated_at")
    ordering = ("name",)
    
    inlines = [RegionInline]

@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    """Admin configuration for the Region model."""
    list_display = ("id", "name", "country", "created_at")
    list_filter = ("country",)
    search_fields = ("name", "country__name") 
    readonly_fields = ("created_at", "updated_at")
    ordering = ("country__name", "name")

    inlines = [DistrictInline]


@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    """Admin configuration for the District model."""
    list_display = ("id", "name", "region", "country_name", "created_at")
    list_filter = ("region__country", "region") 
    search_fields = ("name", "region__name")
    readonly_fields = ("created_at", "updated_at")
    ordering = ("region__name", "name")

    @admin.display(description='Country')
    def country_name(self, obj):
        return obj.region.country.name
    

@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    """Admin configuration for the Currency model."""
    list_display = ("code", "name", "symbol", "unit", "created_at")
    search_fields = ("code", "name", "symbol")
    ordering = ("code",)
    
    fieldsets = (
        (None, {
            'fields': (
                "code", 
                "name", 
                "symbol", 
                "unit"
            ),
        }),
        ('Timestamps', {
            'fields': ("created_at", "updated_at"),
            'classes': ('collapse',),
        })
    )
    

    readonly_fields = ("created_at", "updated_at")