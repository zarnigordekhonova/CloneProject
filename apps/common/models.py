from decimal import Decimal

from django.db import models
from django.utils.translation import gettext_lazy as _


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated at"))

    class Meta:
        abstract = True


class Country(BaseModel):
    name = models.CharField(max_length=64,
                            verbose_name=_("Country name"))
    code = models.CharField(max_length=10, 
                            unique=True,
                            verbose_name=_("Country code"))
    
    class Meta:
        verbose_name = _("Country")
        verbose_name_plural = _("Countries")

    def __str__(self):
        return f"{self.name} - {self.code}"
    

class Region(BaseModel):
    country = models.ForeignKey(Country,
                                on_delete=models.CASCADE,
                                related_name="regions",
                                verbose_name=_("Country"))
    name = models.CharField(max_length=64,
                            verbose_name=_("Region name"))
    
    class Meta:
        verbose_name = _("Region")
        verbose_name_plural = _("Regions")

    def __str__(self):
        return f"{self.name} - {self.country.name}"
    

class District(BaseModel):
    region = models.ForeignKey(Region,
                               on_delete=models.CASCADE,
                               related_name="districts",
                               verbose_name=_("Region"))
    name = models.CharField(max_length=64,
                            verbose_name=_("District name"))
    
    class Meta:
        verbose_name = _("District")
        verbose_name_plural = _("Districts")

    def __str__(self):
        return f"{self.region.name} - {self.name}"
    

class Currency(BaseModel):
    code = models.CharField(max_length=3, 
                            primary_key=True,
                            verbose_name=_("Currency code"))
    name = models.CharField(max_length=32,
                            verbose_name=_("Currency name"))
    symbol = models.CharField(max_length=2,
                              verbose_name=_("Currency symbol"))
    unit = models.DecimalField(max_digits=6,
                               decimal_places=2,
                               default=Decimal("1.00"),
                               verbose_name=_("Smallest currency unit"))
    
    class Meta:
        verbose_name = _("Currency")
        verbose_name_plural = _("Currencies")

    def __str__(self):
        return f"{self.code} - {self.name}"