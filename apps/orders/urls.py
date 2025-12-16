from django.urls import path

from apps.orders.api_endpoint import (
    WindowOrderCreateAPIView,
    DoorOrderCreateAPIView,
    OrderDetailCreateAPIView,
)

app_name = "orders"

urlpatterns = [
    path("window/", WindowOrderCreateAPIView.as_view(), name="window-order-create"),
    path("door/", DoorOrderCreateAPIView.as_view(), name="door-order-create"),
    path("create/", OrderDetailCreateAPIView.as_view(), name="order-detail-create")
]
