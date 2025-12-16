from decimal import Decimal

from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.common.models import BaseModel


class DesignOption(BaseModel):
    name = models.CharField(max_length=32,
                            verbose_name=_("Design Option name"))
    
    class Meta:
        verbose_name = _("Design Option")
        verbose_name_plural = _("Design Options")

    def __str__(self):
        return self.name
    

class DesignVariant(BaseModel):
    option = models.ForeignKey(DesignOption,
                               related_name="variants",
                               on_delete=models.CASCADE,
                               verbose_name=_("Design variant"))
    name = models.CharField(max_length=64,
                            verbose_name=_("Design variant name"))
    image = models.FileField(upload_to="media/materials",
                             null=True,
                             blank=True,
                             verbose_name=_("Design variant image"))
    
    class Meta:
        verbose_name = _("Design Variant")
        verbose_name_plural = _("Design Variants")

    def __str__(self):
        return f"{self.option.name} - {self.name}"
    

class MaterialType(BaseModel):
    name = models.CharField(max_length=64,
                            verbose_name=_("Material name"))
    
    class Meta:
        verbose_name = _("Material Type")
        verbose_name_plural = _("Material Types")

    def __str__(self):
        return self.name
    

class ProfilType(BaseModel):
    material = models.ForeignKey(MaterialType,
                                 on_delete=models.CASCADE,
                                 related_name="profils",
                                 verbose_name=_("Profil material"))
    name = models.CharField(max_length=64,
                            verbose_name=_("Profil name"))
    
    class Meta:
        verbose_name = _("Profil Type")
        verbose_name_plural = _("Profil Types")

    def __str__(self):
        return f"{self.material.name} - {self.name}"
    

class GlassLayer(BaseModel):
    layer = models.CharField(max_length=32,
                             verbose_name=_("Glass layer"))
    
    class Meta:
        verbose_name = _("Glass Layer")
        verbose_name_plural = _("Glass Layers")

    def __str__(self):
        return self.layer
    

class GlassType(BaseModel):
    layer = models.ForeignKey(GlassLayer,
                              on_delete=models.CASCADE,
                              related_name="glasses",
                              verbose_name=_("Glass layer"))
    name = models.CharField(max_length=64,
                            verbose_name=_("Glass type name"))
    price = models.DecimalField(max_digits=9,
                                decimal_places=2,
                                default=Decimal("0.00"),
                                verbose_name=_("Glass type price"))
    currency = models.ForeignKey("common.Currency",
                                 on_delete=models.DO_NOTHING,
                                 verbose_name=_("Glass type currency"))

    class Meta:
        verbose_name = _("Glass Type")
        verbose_name_plural = _("Glass Types")  

    def __str__(self):
        return f"{self.layer.layer} - {self.name}"


class SashProfilType(BaseModel):
    image = models.FileField(upload_to="media/materials",
                             verbose_name=_("Sash profile image"))

    class Meta: 
        verbose_name = _("Sash Profil Types")
        verbose_name_plural = _("Sash Profil Types")

    def __str__(self):
        return self.image.url
    

class FrameProfilType(BaseModel):
    name = models.CharField(max_length=32,
                            verbose_name=_("Frame profil type name"))
    image = models.FileField(upload_to="media/materials",
                             verbose_name=_("Frame profile image"),
                             null=True,
                             blank=True)
    
    class Meta:
        verbose_name = _("Frame Profil Type")
        verbose_name_plural = _("Frame Profil Types")   

    def __str__(self):
        return self.name
    

class HandleType(BaseModel):
    image = models.FileField(upload_to="media/materials",
                             verbose_name=_("Handle type image"))
    
    class Meta:
        verbose_name = _("Handle Type")
        verbose_name_plural = _("Handle Types")

    def __str__(self):
        return self.image.url
    

class Category(BaseModel):
    name = models.CharField(max_length=32,
                            verbose_name=_("Category name"))
    
    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def __str__(self):
        return self.name
    

class Product(BaseModel):
    provider = models.ForeignKey("company.Provider",
                                  on_delete=models.CASCADE,
                                  related_name="products",
                                  verbose_name=_("Product provider"))
    category = models.ForeignKey(Category,
                                on_delete=models.CASCADE,
                                related_name="related_products",
                                verbose_name=_("Product category"),
                                db_index=True)
    material = models.ForeignKey(MaterialType,
                                 on_delete=models.CASCADE,
                                 related_name="relating_products",
                                 verbose_name=_("Product material"))
    design = models.ForeignKey(DesignOption,
                               on_delete=models.CASCADE,
                               related_name="products_designs")
    name = models.CharField(max_length=64,
                            verbose_name=_("Product name"))
    price = models.DecimalField(max_digits=10,
                                decimal_places=2,
                                verbose_name=_("Product price"))
    image = models.FileField(upload_to="media/products",
                             null=True, 
                             blank=True,
                             verbose_name=_("Product image"))
    
    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")

    def __str__(self):
        return f"{self.provider.name} - {self.material.name} - {self.name}"
    

class CustomProduct(BaseModel):
    class MeasurementUnitChoices(models.TextChoices):
        PIECE = "PIECE", _("Piece")
        LENGTH = "LENGTH", _("Length")

    category = models.ForeignKey(Category,
                                 on_delete=models.CASCADE,
                                 related_name="products",
                                 verbose_name=_("Product category"))
    provider_name = models.CharField(max_length=64,
                                     verbose_name=_("Provider name"))
    name = models.CharField(max_length=64,
                            verbose_name=_("Product name"))
    measurement_unit = models.CharField(max_length=32,
                                        choices=MeasurementUnitChoices.choices,
                                        default=MeasurementUnitChoices.PIECE,
                                        verbose_name=_("Measurement unit"))
    measurement_value = models.DecimalField(max_digits=4,
                                            decimal_places=2,
                                            verbose_name=_("Measurement value"))
    ordinary_price = models.DecimalField(max_digits=9,
                                         decimal_places=2,
                                         default=Decimal("0.00"),
                                         verbose_name=_("Price per ordinary product"))
    colorful_price =  models.DecimalField(max_digits=9,
                                          decimal_places=2,
                                          default=Decimal("0.00"),
                                          verbose_name=_("Price per colorful product"))
    image = models.FileField(upload_to="media/products",
                             null=True,
                             blank=True,
                             verbose_name=_("Product image"))
    
    class Meta:
        verbose_name = _("Custom Product")
        verbose_name_plural = _("Custom Products")

    def __str__(self):
        return f"{self.provider_name} - {self.name}"

