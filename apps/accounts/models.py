from django.db import models
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from django.utils import timezone

from apps.common.models import BaseModel
from apps.accounts.managers import CustomUserManager


class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    full_name = models.CharField(max_length=256,
                                 verbose_name=_("Full name"),
                                 help_text=_("User's full name"))
    phone_number = models.CharField(
        max_length=14,  
        validators=[
            RegexValidator(
                regex=r"^\+998\d{9}$",
            )
        ],
        unique=True,
        db_index=True,
        verbose_name=_("Phone number"))
    country = models.ForeignKey("common.Country",
                                on_delete=models.DO_NOTHING,
                                related_name="users",
                                null=True,
                                blank=True,
                                verbose_name=_("User country"))
    is_active = models.BooleanField(default=True,
                                    verbose_name=_("Active status"),
                                    db_index=True)
    is_confirmed = models.BooleanField(default=False, verbose_name=_("Is Confirmed"))
    is_staff = models.BooleanField(default=False, verbose_name=_("Is Staff"))
    is_deleted = models.BooleanField(default=False,
                                     verbose_name=_("Deleted status"),
                                     db_index=True)
    deleted_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Deleted at"),
        help_text=_("Timestamp when user was deleted")
    )
    
    objects = CustomUserManager()
    
    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = [
        "full_name", 
    ]

    def __str__(self):
        if self.full_name:
            return f"{self.full_name}"
        return self.phone_number
    
    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")
        constraints = [
            models.UniqueConstraint(
                fields=["phone_number"],
                condition=models.Q(is_deleted=False),
                name="unique_active_phone_number",
            ),
        ]

    def delete_account(self):
        """Soft delete user account"""
        timestamp = int(timezone.now().timestamp())
        
        self.phone_number = f"{self.phone_number}_deleted_{timestamp}"
        self.is_deleted = True
        self.is_active = False
        self.deleted_at = timezone.now()
        
        self.save(update_fields=["phone_number", "is_deleted", "is_active", "deleted_at"])


class Employee(BaseModel):

    class ProfessionsChoices(models.TextChoices):
        ORDER_RECIPIENT = "ORDER_RECIPIENT", _("Order_recipient") # buyurtma oluvchi
        COLLECTOR = "COLLECTOR", _("Collector") # yig'uvchi
        INSTALLER = "INSTALLER", _("Installer") # o'rnatib beruvchi
        DRIVER = "DRIVER", _("Driver") # haydovchi
        GLASS_CUTTER = "GLASS_CUTTER", _("Glass_cutter")

    full_name = models.CharField(max_length=64,
                                    verbose_name=_("Full name"),
                                    help_text="Employee's full name.")
    phone_number = models.CharField(max_length=14,  
                                    validators=[
                                        RegexValidator(
                                            regex=r"^\+998\d{9}$",
                                        )
                                    ],
                                    db_index=True,
                                    verbose_name=_("Phone number"))
    profession = models.CharField(max_length=64,
                                  choices=ProfessionsChoices.choices,
                                  verbose_name=_("Employee profession"))
    share = models.FloatField(verbose_name=_("Share"),
                              help_text=_("Employee's share"))
    employer = models.ForeignKey(User,
                                 on_delete=models.CASCADE,
                                 verbose_name=_("Employer"))
    
    @property
    def total_salary(self):
        return self.payments.aggregate(
            total=models.Sum("amount")
        )["total"] or 0
    
    def __str__(self):
        return self.full_name
    
    class Meta:
        verbose_name = _("Employee")
        verbose_name_plural = _("Employees")


class EmployeePayment(BaseModel):
    employee = models.ForeignKey(Employee,
                                 on_delete=models.CASCADE,
                                 related_name="payments",
                                 verbose_name=_("Related employee"))
    amount = models.DecimalField(max_digits=11, 
                                 decimal_places=2,
                                 verbose_name=_("Amount"))
    
    def __str__(self):
        return self.employee.full_name
    
    class Meta:
        verbose_name = _("Employee Payment")
        verbose_name_plural = _("Employee Payments")
    
    


    