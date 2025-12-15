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


# NEW MODELS

# Umumiy deraza/eshik/fortochka shablonlari uchun model
class Template(BaseModel):
    
    class TemplateType(models.TextChoices):
        WINDOW = "WINDOW", _("Window")
        DOOR = "DOOR", _("Door")
        FORTOCHKA = "FORTOCHKA", _("Fortochka")

    name = models.CharField(max_length=128, 
                            null=True,
                            blank=True,
                            verbose_name=_("Template name"))
    template_type = models.CharField(max_length=32,
                                     choices=TemplateType.choices,
                                     verbose_name=_("Template type"))
    # eni hajmi
    base_width_mm = models.PositiveIntegerField(verbose_name=_("Base width"))
    # bo'yi hajmi
    base_height_mm = models.PositiveSmallIntegerField(verbose_name=_("Base height"))
    # narxi metr kvadratga qarab belgilanadi
    base_price_per_m2 = models.DecimalField(max_digits=10,
                                            decimal_places=2,
                                            verbose_name=_("Base price"),
                                            help_text=_("Window/Door/Fortochka's base price per m2."))
    
    def __str__(self):
        return self.name if self.name else self.id
    
    class Meta:
        verbose_name = _("Template")
        verbose_name_plural = _("Templates")
        constraints = [
            models.UniqueConstraint(
                fields=["name", "template_type"],
                name="unique_name_per_template_type"
            )
        ]


# Bu shablonni ichidagi qismlari uchun model
class TemplateSection(BaseModel):

    class SectionType(models.TextChoices):
        TOP = "TOP", _("Top")
        MIDDLE = "MIDDLE", _("Middle")
        BOTTOM = "BOTTOM", _("Bottom")
        WHOLE = "WHOLE", _("Whole")

    class OrientationType(models.TextChoices):
        VERTICAL = "VERTICAL", _("Vertical")
        HORIZONTAL = "HORIZONTAL", _("Horizontal")

    template = models.ForeignKey(Template,
                                 on_delete=models.CASCADE,
                                 related_name="sections",
                                 verbose_name=_("Related template"))
    has_glass = models.BooleanField(default=True,
                                    verbose_name=_("Has section glass"))
    section_type = models.CharField(max_length=32,
                                    choices=SectionType.choices,
                                    verbose_name=_("Section type"))
    # har bitta qismni tartib raqami
    section_order = models.PositiveIntegerField(verbose_name=_("Section order number"))
    # qism vertikal/gorizontal tushishini belgilash uchun
    orientation = models.CharField(max_length=15, 
                                   choices=OrientationType.choices,
                                   verbose_name=_("Orientation type"))
    # o'sha qismni eni hajmi
    # admin panelda, bu field uchun qiymat 0-1 oralig'ida kiritilishi kerak, ya'ni
    # agar eni yarim metr bo'lsa, millimetrda 500 emas, 0.5 sifatida berish kerak
    width_ratio = models.FloatField(null=True,
                                    blank=True,
                                    verbose_name=_("Section's width size"))
    # bo'yi hajmi
    # height_ratio uchun ham qiymat 0-1 oralig'ida berilishi kerak
    height_ratio = models.FloatField(null=True,
                                    blank=True,
                                    verbose_name=_("Section's height size"))
    
    def __str__(self):
        return f"Section {self.section_order} of {self.template.name}"
    
    class Meta:
        verbose_name = _("Template Section")
        verbose_name_plural = _("Template Sections")


# Bunda foydalanuvchi buyurtmasi saqlanadi, foydalanuvchi shablonni idsini,
# uni eni, bo'yi hajmini kiritadi, umumiy narxi avtomatik hisoblanadi. 
class WindowOrder(BaseModel):
    template = models.ForeignKey(Template,
                                 on_delete=models.CASCADE,
                                 verbose_name=_("Template"))
    width_mm = models.PositiveIntegerField(verbose_name=_("Order's width size."))
    height_mm = models.PositiveIntegerField(verbose_name=_("Order's height size."))
    total_price = models.DecimalField(max_digits=12, 
                                      decimal_places=2,
                                      blank=True,
                                      verbose_name=_("Order's total price"))
    
    class Meta:
        verbose_name = _("Window Order")
        verbose_name_plural = _("Window Orders")
    
    def calculate_area_m2(self):
        width_m = Decimal(self.width_mm) / Decimal(1000)
        height_m = Decimal(self.height_mm) / Decimal(1000)
        return width_m * height_m
    
    def calculate_price(self):
        area = self.calculate_area_m2()
        return area * self.template.base_price_per_m2
    
    def save(self, *args, **kwargs):
        self.total_price = self.calculate_price()
        super().save(*args, **kwargs)


# Bu modelda agar foydalanuvchi shablondagi qismlarni eni va hajmini ham o'zi
# o'zgartirib kiritsa, shu qismlarni ma'lumoti saqlanadi
class WindowOrderSection(BaseModel):
    order = models.ForeignKey(WindowOrder,
                              on_delete=models.CASCADE,
                              related_name="sections",
                              verbose_name=_("Related order"))
    # Haqiqiy shablondagi qaysi qismga bog'lanyapti
    template_section = models.ForeignKey(TemplateSection,
                                         on_delete=models.SET_NULL,
                                         null=True,
                                         blank=True,
                                         related_name="order_sections",
                                         verbose_name=_("Original template section"))
    section_order = models.PositiveIntegerField(verbose_name=_("Section order number"))
    width_mm = models.PositiveIntegerField(null=True,
                                           blank=True,
                                           verbose_name=_("Section width in mm"))
    height_mm = models.PositiveIntegerField(null=True,
                                            blank=True,
                                            verbose_name=_("Section height in mm"))
    # O'sha qismni yuzasi uchun
    area_m2 = models.DecimalField(max_digits=10,
                                  decimal_places=4,
                                  verbose_name=_("Area m²"))

    class Meta:
        verbose_name = _("Window order section")
        verbose_name_plural = _("Window order sections")

    def __str__(self):
        return f"Section {self.section_order} of Order {self.order_id}"

    @property
    def area_m2(self):
        width_m = Decimal(self.width_mm) / Decimal(1000)
        height_m = Decimal(self.height_mm) / Decimal(1000)
        return width_m * height_m


# Door models
class DoorOrder(BaseModel):
    template = models.ForeignKey(Template,
                                 on_delete=models.CASCADE,
                                 verbose_name=_("Template"))
    width_mm = models.PositiveIntegerField(verbose_name=_("Order's width size."))
    height_mm = models.PositiveIntegerField(verbose_name=_("Order's height size."))
    total_price = models.DecimalField(max_digits=12, 
                                      decimal_places=2,
                                      blank=True,
                                      verbose_name=_("Order's total price"))
    
    class Meta:
        verbose_name = _("Door Order")
        verbose_name_plural = _("Door Orders")
    
    def calculate_area_m2(self):
        width_m = Decimal(self.width_mm) / Decimal(1000)
        height_m = Decimal(self.height_mm) / Decimal(1000)
        return width_m * height_m
    
    def calculate_price(self):
        area = self.calculate_area_m2()
        return area * self.template.base_price_per_m2
    
    def save(self, *args, **kwargs):
        self.total_price = self.calculate_price()
        super().save(*args, **kwargs)


class DoorOrderSection(BaseModel):
    order = models.ForeignKey(DoorOrder,
                              on_delete=models.CASCADE,
                              related_name="door_sections",
                              verbose_name=_("Related order"))
    # Haqiqiy shablondagi qaysi qismga bog'lanyapti
    template_section = models.ForeignKey(TemplateSection,
                                         on_delete=models.SET_NULL,
                                         null=True,
                                         blank=True,
                                         related_name="door_order_sections",
                                         verbose_name=_("Original template section"))
    section_order = models.PositiveIntegerField(verbose_name=_("Section order number"))
    width_mm = models.PositiveIntegerField(null=True,
                                           blank=True,
                                           verbose_name=_("Section width in mm"))
    height_mm = models.PositiveIntegerField(null=True,
                                            blank=True,
                                            verbose_name=_("Section height in mm"))
    # O'sha qismni yuzasi uchun
    area_m2 = models.DecimalField(max_digits=10,
                                  decimal_places=4,
                                  verbose_name=_("Area m²"))

    class Meta:
        verbose_name = _("Door order section")
        verbose_name_plural = _("Door order sections")

    def __str__(self):
        return f"Section {self.section_order} of Order {self.order_id}"

    @property
    def area_m2(self):
        width_m = Decimal(self.width_mm) / Decimal(1000)
        height_m = Decimal(self.height_mm) / Decimal(1000)
        return width_m * height_m
