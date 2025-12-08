# from django.contrib import admin
# from django.utils.translation import gettext_lazy as _
# from django.core.exceptions import ValidationError

# from apps.orders.models import NewOrder, OrderDetail, Order


# class OrderDetailInline(admin.TabularInline):
#     model = OrderDetail
#     extra = 1
    
#     raw_id_fields = (
#         'material', 
#         'glass_layer', 
#         'glass_type', 
#         'provider', 
#         'profil_type', 
#         'sash_profil_type', 
#         'frame_profile_type', 
#         'design_option', 
#         'design_variant', 
#         'handle_type'
#     )
    
#     fieldsets = (
#         (None, {
#             'fields': (
#                 ("height_size", "width_size"),
#                 ("material", "provider", "profil_type"),
#             )
#         }),
#         (_("Glass & Design"), {
#             'fields': (
#                 ("glass_layer", "glass_type"),
#                 ("design_option", "design_variant"),
#             )
#         }),
#         (_("Accessories & Metal"), {
#             'fields': (
#                 ("sash_profil_type", "frame_profile_type"),
#                 ("has_handle", "handle_type"),
#                 "shelf_width",
#                 ("has_metal", "metal_thickness"),
#                 "has_balcony",
#             )
#         }),
#         (_("Waste Calculation"), {
#             'fields': (
#                 ("include_waster_percentage", "waste_percentage"),
#             )
#         }),
#     )

# class NewOrderInline(admin.TabularInline):
#     model = NewOrder
#     extra = 0 
#     readonly_fields = ("order_number", "total_price", "cost_price", "profit", "discount_price", "advance_payment")
    
#     list_display = (
#         "id",
#         "order_type", 
#         "order_number", 
#         "quantity", 
#         "total_price", 
#         "profit", 
#         "order_owner"
#     )


# @admin.register(NewOrder)
# class NewOrderAdmin(admin.ModelAdmin):
#     list_display = (
#         "id",
#         "order_number", 
#         "order_type", 
#         "order_owner", 
#         "phone_number", 
#         "total_price", 
#         "profit",
#         "created_at",
#     )
#     list_filter = ("order_type", "created_at")
#     search_fields = ("order_number", "order_owner", "phone_number")
    
#     fieldsets = (
#         (None, {
#             'fields': (
#                 ("order_type", "order_number"),
#                 "quantity",
#             )
#         }),
#         (_("Customer Info & Location"), {
#             'fields': ("order_owner", "phone_number", "location", "additional_info"),
#         }),
#         (_("Financial Summary"), {
#             'fields': (
#                 "total_price", 
#                 "cost_price", 
#                 "profit", 
#                 "discount_price", 
#                 "advance_payment"
#             ),
#         }),
#         (_("Timestamps"), {
#             'fields': ("created_at", "updated_at"),
#             'classes': ('collapse',),
#         })
#     )
    
#     readonly_fields = ("created_at", "updated_at", "profit") # Profit is typically calculated
#     inlines = [OrderDetailInline]


# @admin.register(OrderDetail)
# class OrderDetailAdmin(admin.ModelAdmin):
#     list_display = (
#         "id", 
#         "order_number_display", 
#         "material", 
#         "height_size", 
#         "width_size", 
#         "has_metal", 
#         "has_handle"
#     )
#     list_filter = (
#         "material", 
#         "glass_layer", 
#         "provider", 
#         "has_balcony", 
#         "has_metal", 
#         "has_handle"
#     )
#     search_fields = (
#         "order__order_number",
#         "material__name",
#         "provider__name",
#     )
#     readonly_fields = ("created_at", "updated_at")

#     @admin.display(description=_("Order Number"))
#     def order_number_display(self, obj):
#         return obj.order.order_number


# @admin.register(Order)
# class OrderAdmin(admin.ModelAdmin):
#     list_display = (
#         "id",
#         "total_orders_number", 
#         "total_price", 
#         "status", 
#         "created_at"
#     )
#     list_filter = ("status", "created_at")
#     search_fields = ("status",)
#     readonly_fields = ("created_at", "updated_at")
    
#     inlines = [NewOrderInline]

#     fieldsets = (
#         (None, {
#             'fields': (
#                 "status", 
#                 "total_orders_number", 
#                 "total_price"
#             ),
#         }),
#         (_("Timestamps"), {
#             'fields': ("created_at", "updated_at"),
#             'classes': ('collapse',),
#         })
#     )