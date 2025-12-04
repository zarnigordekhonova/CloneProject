from decimal import Decimal

from django.db import models
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _

from apps.common.models import BaseModel


class NewOrder(BaseModel):
    class OrderTypeChoices(models.TextChoices):
        WINDOW = "WINDOW", _("Window")
        DOOR = "DOOR", _("Door")
        FORTOCHKA = "FORTOCHKA", _("Fortochka")

    order_type = models.CharField(max_length=32,
                                  choices=OrderTypeChoices.choices,
                                  verbose_name=_("Order type"))
    order_number = models.CharField(max_length=32,
                                    unique=True,
                                    verbose_name=_("Order number"))
    quantity = models.PositiveIntegerField(verbose_name=_("Order quantity"))
    total_price = models.DecimalField(max_digits=11,
                                      decimal_places=2,
                                      verbose_name=_("Order's total price"))
    # tannarx
    cost_price = models.DecimalField(max_digits=11,
                                     decimal_places=2,
                                     verbose_name=_("Cost price of order"))
    # foyda
    profit = models.DecimalField(max_digits=11,
                                 decimal_places=2,
                                 verbose_name=_("Profit from the order"))
    discount_price = models.DecimalField(max_digits=11,
                                         decimal_places=2,
                                         null=True,
                                         blank=True,
                                         verbose_name=_("Discount price"))
    # avans
    advance_payment = models.DecimalField(max_digits=11,
                                          decimal_places=2,
                                          verbose_name=_("Advance payment"))
    order_owner = models.CharField(max_length=64,
                                   verbose_name=_("Owner name"))
    phone_number = models.CharField(
        max_length=50,  
        validators=[
            RegexValidator(
                regex=r"^\+998\d{9}$",
            )
        ],
        verbose_name=_("Phone number"))
    location = models.TextField(verbose_name=_("Location"))
    additional_info = models.TextField(verbose_name=_("Additional info"))

    class Meta:
        verbose_name = _("New Order")
        verbose_name_plural = _("New Orders")

    def __str__(self):
        return f"{self.order_type} - {self.total_price}"
    

class OrderDetail(BaseModel):
    class MetalThicknessChoices(models.TextChoices):
        OPTION_1 = "1.0 mm", _("1.0 mm")
        OPTION_2 = "1.2 mm", _("1.2 mm")


    order = models.ForeignKey(NewOrder,
                              on_delete=models.CASCADE,
                              related_name="order_detail",
                              verbose_name=_("Main order"))
    height_size = models.FloatField(verbose_name=_("Order's height size"))
    width_size = models.FloatField(verbose_name=_("Order's width size"))
    material = models.ForeignKey("materials.MaterialType",
                                 on_delete=models.DO_NOTHING,
                                 verbose_name=_("Order material"))
    glass_layer = models.ForeignKey("materials.GlassLayer",
                                    on_delete=models.DO_NOTHING,
                                    verbose_name=_("Order's glass layer"))
    glass_type = models.ForeignKey("materials.GlassType",
                                   on_delete=models.DO_NOTHING,
                                   verbose_name=_("Order's glass type"))
    provider = models.ForeignKey("company.Provider",
                                 on_delete=models.DO_NOTHING,
                                  verbose_name=_("Provider"))
    include_waster_percentage = models.BooleanField(default=True,
                                                    verbose_name=_("Include waste percentage"))
    waste_percentage = models.FloatField(null=True,
                                         blank=True,
                                         verbose_name=_("Waste percentage"))
    profil_type = models.ForeignKey("materials.ProfilType",
                                    on_delete=models.DO_NOTHING,
                                    verbose_name=_("Order's profil type"))
    has_balcony = models.BooleanField(default=False,
                                      verbose_name=_("Order's balcony"))
    has_metal = models.BooleanField(default=False,
                                    verbose_name=_("Order's metal"))
    metal_thickness = models.CharField(max_length=32,
                                       choices=MetalThicknessChoices.choices,
                                       null=True,
                                       blank=True,
                                       verbose_name=_("Metal thickness"))
    sash_profil_type = models.ForeignKey("materials.SashProfilType",
                                         on_delete=models.DO_NOTHING,
                                         verbose_name=_("Sash profil type"))
    frame_profile_type = models.ForeignKey("materials.FrameProfilType",
                                           on_delete=models.DO_NOTHING,
                                           verbose_name=_("Frame profil type"))
    design_option = models.ForeignKey("materials.DesignOption",
                                      on_delete=models.DO_NOTHING,
                                      verbose_name=_("Order design option"))
    design_variant = models.ForeignKey("materials.DesignVariant",
                                       on_delete=models.DO_NOTHING,
                                       verbose_name=_("Order design variant"))
    shelf_width = models.FloatField(verbose_name=_("Shelf width"))
    has_handle = models.BooleanField(default=False,
                                     verbose_name=_("Order handle"))
    handle_type = models.ForeignKey("materials.HandleType",
                                    on_delete=models.DO_NOTHING,
                                    verbose_name=_("Order's handle type"))
    
    class Meta:
        verbose_name = _("Order Detail")
        verbose_name_plural = _("Order Details")

    def __str__(self):
        return self.order
    

class Order(BaseModel):
    class OrderStatusChoices(models.TextChoices):
        WAITING = "WAITING", _("Waiting")
        CLOSED = "CLOSED", _("Closed")
        IN_PROCESS = "IN_PROCESS", _("In_process")
        IN_DEBT = "IN_DEBT", _("In_debt")

    total_orders_number = models.PositiveIntegerField(verbose_name=_("Total number of orders"))
    total_price = models.DecimalField(max_digits=11,
                                      decimal_places=2,
                                      verbose_name=_("Total price of orders"))
    status = models.CharField(max_length=32,
                              choices=OrderStatusChoices.choices,
                              default=OrderStatusChoices.WAITING,
                              verbose_name=_("Order status"))
    