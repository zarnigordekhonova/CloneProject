from django.contrib import admin, messages
from django.db import transaction
from django.utils import timezone
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

@admin.action(description="Delete (soft) selected users")
def deactivate_users(modeladmin, request, queryset):
    """Custom admin action to soft delete users"""
    deactivated_count = 0

    with transaction.atomic():
        for user in queryset:
            if not user.is_deleted:  # Only deactivate active users
                timestamp = int(timezone.now().timestamp())
               
                max_email_length = 128 - len(f"_deleted_{timestamp}") - 1
                base_email = user.email[:max_email_length] if len(user.email) > max_email_length else user.email
                
                max_username_length = 128 - len(f"_del_{timestamp}") - 1
                base_username = user.username[:max_username_length] if len(user.username) > max_username_length else user.username
        
                # Update using queryset to bypass validation
                CustomUser.objects.filter(pk=user.pk).update(
                    email=f"{base_email}_deleted_{timestamp}",
                    username=f"{base_username}_del_{timestamp}",
                    is_deleted=True,
                    is_active=False,  # Also deactivate
                    deleted_at = timezone.now()
                )
                deactivated_count += 1

    messages.success(request, f"Successfully deactivated {deactivated_count} user(s).")