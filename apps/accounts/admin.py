from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

from .actions import deactivate_users
from apps.accounts.models import Employee

User = get_user_model()

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = (
        "id",
        "phone_number",
        "full_name",
        "country",
        "is_confirmed",
        "is_active",
        "is_staff",
        "is_deleted", 
        "created_at",
    )
    
    list_filter = (
        "is_staff",
        "is_active",
        "is_confirmed",
        "is_deleted",
        "country",
        "created_at",
    )
    
    search_fields = (
        "phone_number",
        "full_name",
    )

    fieldsets = (
        (
            None, 
            {
                "fields": ("phone_number", "password"),
            }
        ),
        (
            _("Personal Info"), 
            {
                "fields": ("full_name", "country"),
            }
        ),
        (
            _("Permissions & Status"), 
            {
                "fields": (
                    "is_active",
                    "is_confirmed",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            }
        ),
        (
            _("Soft-Delete Status"), 
            {
                "fields": ("is_deleted", "deleted_at"),
                "classes": ("collapse",) 
            }
        ),
        (
            _("Important Dates"), 
            {
                "fields": ("created_at", "updated_at", "last_login",),
                "classes": ("collapse",)
            }
        ),
    )
    
    readonly_fields = (
        "created_at", 
        "updated_at", 
        "last_login", 
        "is_deleted",
        "deleted_at",
    )
    ordering = ("-created_at",)

    actions = [deactivate_users, ]

    
# admin.py
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Employee


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    
    # Fields displayed in list view
    list_display = (
        'id',
        'full_name',
        'phone_number',
        'profession',
        'share',
        'total_share',
        'employer',
        'created_at',
    )
    
    list_display_links = ('full_name', 'phone_number')
    
    list_filter = (
        'profession',
        'employer',
        'created_at',
    )
    
    search_fields = (
        'full_name',
        'phone_number',
        'employer__full_name',  
    )
    
    readonly_fields = (
        'created_at',
        'updated_at',
        'total_share',  
    )
    
    fieldsets = (
        (_('Personal Information'), {
            'fields': ('full_name', 'phone_number')
        }),
        (_('Professional Details'), {
            'fields': ('profession', 'share', 'total_share')
        }),
        (_('Employer'), {
            'fields': ('employer',)
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)  
        }),
    )
    
    ordering = ('-created_at',)
    
    list_per_page = 25
    
    actions = ['mark_as_active', 'mark_as_inactive']
    
    def mark_as_active(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} employees activated.')
    mark_as_active.short_description = _("Mark selected as active")
    
    def mark_as_inactive(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} employees deactivated.')
    mark_as_inactive.short_description = _("Mark selected as inactive")
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs
    
    def save_model(self, request, obj, form, change):
        if not change:  
            obj.employer = request.user
        super().save_model(request, obj, form, change)