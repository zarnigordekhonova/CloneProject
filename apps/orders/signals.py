from decimal import Decimal

from django.dispatch import receiver
from django.db.models.signals import post_save

from apps.orders.models import OrderDetail, Order


@receiver(post_save, sender=OrderDetail)
def create_order_record(sender, instance, created, **kwargs):
    window_order = instance.window_order
    # door_order = instance.door_order
    
    if window_order:
        total_price = window_order.total_price
    else:
        total_price = Decimal("0.00")

    last_order = Order.objects.last()
    next_order = (last_order.total_orders_number + 1) if last_order else 1

    if created:
        Order.objects.create(
            order=instance,
            total_orders_number=next_order,
            total_price=total_price,
            status=Order.OrderStatusChoices.WAITING
        )
