from decimal import Decimal

from django.db import models 
from django.utils.translation import gettext_lazy as _

from apps.common.models import BaseModel


class Dealer(BaseModel):
    name = models.CharField(max_length=255,
                            verbose_name=_("Dealer name"))
    
    class Meta:
        verbose_name = _("Dealer")
        verbose_name_plural = _("Dealers")

    def __str__(self):
        return self.name
    

class Company(BaseModel):
    region = models.ForeignKey("common.Region",
                               on_delete=models.CASCADE,
                               verbose_name=_("Company region"))
    district = models.ForeignKey("common.District",
                                 on_delete=models.CASCADE,
                                 verbose_name=_("Company district"))
    dealer = models.ForeignKey(Dealer,
                               on_delete=models.DO_NOTHING,
                               verbose_name=_("Company dealer"))
    free_delivery = models.BooleanField(default=True,
                                        verbose_name=_("Free delivery"))
    telegram_link = models.CharField(max_length=32,
                                     null=True,
                                     blank=True,
                                     verbose_name=_("Telegram group link"))
    
    class Meta:
        verbose_name = _("Company")
        verbose_name_plural = _("Companies")

    def __str__(self):
        return self.dealer.name
    

class ProductConfig(BaseModel):
    class ProductType(models.TextChoices):
        ALUMIN = "ALUMIN", _("Alumin")
        PLAST = "PLAST", _("Plast")
        THERMO = "THERMO", _("Thermo")

    company = models.ForeignKey(Company,
                                on_delete=models.CASCADE,
                                related_name="product",
                                verbose_name=_("Related company"))
    product_type = models.CharField(max_length=32,
                                    choices=ProductType.choices,
                                    verbose_name=_("Product type"))
    is_in_percentage = models.BooleanField(default=True,
                                           verbose_name=_("Profit by percentage"))
    is_in_meter = models.BooleanField(default=False,
                                      verbose_name=_("Profit by meter"))
    profit = models.DecimalField(max_digits=6,
                                 decimal_places=2,
                                 default=Decimal("50.0"),
                                 verbose_name=_("Profit amount"))
    currency = models.ForeignKey("common.Currency",
                                    on_delete=models.DO_NOTHING,
                                    verbose_name=_("Profit currency"))
    
    class Meta:
        verbose_name = _("Product configuration")
        verbose_name_plural = _("Product configurations")
        constraints = (
            models.UniqueConstraint(fields=["company", "product_type"],
                                    name="unique_company_product_type"),
        )

    def __str__(self):
        return f"{self.company.dealer.name} - {self.product_type}"
    

class Provider(BaseModel):
    name = models.CharField(max_length=64,
                            verbose_name=_("Provider name"),
                            db_index=True)
    logo = models.FileField(upload_to="media/logo",
                            null=True,
                            blank=True,
                            verbose_name=_("Provider logo"))
    
    class Meta:
        verbose_name = _("Provider")
        verbose_name_plural = _("Providers")

    def __str__(self):
        return self.name
