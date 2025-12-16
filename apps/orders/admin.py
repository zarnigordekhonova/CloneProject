from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

from apps.orders.models import (NewOrder, 
                                OrderDetail, 
                                Order, 
                                WindowOrder, 
                                Template, 
                                TemplateSection,
                                WindowOrderSection, 
                                DoorOrder,
                                DoorOrderSection)


class OrderDetailInline(admin.TabularInline):
    model = OrderDetail
    extra = 1
    
    raw_id_fields = (
        'material', 
        'glass_layer', 
        'glass_type', 
        'provider', 
        'profil_type', 
        'sash_profil_type', 
        'frame_profile_type', 
        'design_option', 
        'design_variant', 
        'handle_type',
        'window_order',
    )
    
    fieldsets = (
        (None, {
            'fields': (
                ("material", "provider", "profil_type"),
                 "window_order",
            )
        }),
        (_("Glass & Design"), {
            'fields': (
                ("glass_layer", "glass_type"),
                ("design_option", "design_variant"),
            )
        }),
        (_("Accessories & Metal"), {
            'fields': (
                ("sash_profil_type", "frame_profile_type"),
                ("has_handle", "handle_type"),
                "shelf_width",
                ("has_metal", "metal_thickness"),
                "has_balcony",
            )
        }),
        (_("Waste Calculation"), {
            'fields': (
                ("include_waste_percentage", "waste_percentage"),
            )
        }),
    )

class NewOrderInline(admin.TabularInline):
    model = NewOrder
    extra = 0 
    readonly_fields = ("order_number", "total_price", "cost_price", "profit", "discount_price", "advance_payment")
    
    list_display = (
        "id",
        "order_type", 
        "order_number", 
        "quantity", 
        "total_price", 
        "profit", 
        "order_owner"
    )


@admin.register(NewOrder)
class NewOrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "order_number", 
        "order_type", 
        "order_owner", 
        "phone_number", 
        "total_price", 
        "profit",
        "created_at",
    )
    list_filter = ("order_type", "created_at")
    search_fields = ("order_number", "order_owner", "phone_number")
    
    fieldsets = (
        (None, {
            'fields': (
                ("order_type", "order_number"),
                "quantity",
            )
        }),
        (_("Customer Info & Location"), {
            'fields': ("order_owner", "phone_number", "location", "additional_info"),
        }),
        (_("Financial Summary"), {
            'fields': (
                "total_price", 
                "cost_price", 
                "profit", 
                "discount_price", 
                "advance_payment"
            ),
        }),
        (_("Timestamps"), {
            'fields': ("created_at", "updated_at"),
            'classes': ('collapse',),
        })
    )
    
    readonly_fields = ("created_at", "updated_at", "profit") # Profit is typically calculated
    inlines = [OrderDetailInline]


@admin.register(OrderDetail)
class OrderDetailAdmin(admin.ModelAdmin):
    list_display = (
        "id", 
        "order_number_display", 
        "window_order",
        "material", 
        "has_metal", 
        "has_handle"
    )
    list_filter = (
        "material", 
        "glass_layer", 
        "provider", 
        "has_balcony", 
        "has_metal", 
        "has_handle"
    )
    search_fields = (
        "order__order_number",
        "material__name",
        "provider__name",
    )
    readonly_fields = ("created_at", "updated_at")

    @admin.display(description=_("Order Number"))
    def order_number_display(self, obj):
        return obj.order.order_number


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "total_orders_number", 
        "total_price", 
        "status", 
        "created_at"
    )
    list_filter = ("status", "created_at")
    search_fields = ("status",)
    readonly_fields = ("created_at", "updated_at")
    
    # inlines = [NewOrderInline]

    fieldsets = (
        (None, {
            'fields': (
                "status", 
                "total_orders_number", 
                "total_price"
            ),
        }),
        (_("Timestamps"), {
            'fields': ("created_at", "updated_at"),
            'classes': ('collapse',),
        })
    )


class TemplateSectionInline(admin.TabularInline):
    model = TemplateSection
    extra = 1  
    fields = ('section_order', 'has_glass', 'section_type', 'orientation', 'width_ratio', 'height_ratio')


@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name', 
        'template_type',
        'base_width_mm', 
        'base_height_mm', 
        'base_price_per_m2'
    )
    search_fields = ('name',)
    inlines = [TemplateSectionInline]


@admin.register(WindowOrder)
class WindowOrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'template', 
        'width_mm', 
        'height_mm', 
        'total_price', 
        'display_area'
    )
    list_filter = ('template',)
    search_fields = (
        'template__name', 
        'width_mm', 
        'height_mm'
    )
    
    def display_area(self, obj):
        return f"{obj.calculate_area_m2():.2f} m²"
    display_area.short_description = "Area (m²)"


@admin.register(TemplateSection)
class TemplateSectionAdmin(admin.ModelAdmin):
    list_display = ('id', 'template', 'section_type', 'has_glass', 'section_order', 'orientation', 'width_ratio', 'height_ratio')
    list_filter = ('template', 'orientation')
    search_fields = ('template__name',)


@admin.register(WindowOrderSection)
class WindowOrderSectionAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'order', 
        'section_order', 
        'width_mm', 
        'height_mm', 
        'area_m2'
    )
    
    list_filter = (
        'order__template', 
        'order',           
    )
    
    search_fields = (
        'order__id', 
        'order__template__name'
    )
    
    readonly_fields = (
        'area_m2',
    )
    
    fieldsets = (
        (None, {
            'fields': ('order', 'template_section', 'section_order')
        }),
        ('Dimensions and Area', {
            'fields': ('width_mm', 'height_mm', 'area_m2')
        }),
    )


@admin.register(DoorOrder)
class DoorOrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'template', 
        'width_mm', 
        'height_mm', 
        'total_price', 
        'display_area'
    )
    list_filter = ('template',)
    search_fields = (
        'template__name', 
        'width_mm', 
        'height_mm'
    )
    readonly_fields = (
        'total_price', 
        'display_area'
    )
    
    def display_area(self, obj):
        return f"{obj.calculate_area_m2():.2f} m²"
    display_area.short_description = "Area (m²)"


@admin.register(DoorOrderSection)
class DoorOrderSectionAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'order', 
        'section_order', 
        'width_mm', 
        'height_mm', 
        'area_m2'
    )
    
    list_filter = (
        'order__template', 
        'order',           
    )
    
    search_fields = (
        'order__id', 
        'order__template__name'
    )
    
    readonly_fields = (
        'area_m2',
    )
    
    fieldsets = (
        (None, {
            'fields': ('order', 'template_section', 'section_order')
        }),
        ('Dimensions and Area', {
            'fields': ('width_mm', 'height_mm', 'area_m2')
        }),
    )