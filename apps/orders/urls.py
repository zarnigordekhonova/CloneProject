from django.urls import path

from apps.orders.api_endpoint import (
    WindowOrderCreateAPIView,
)

app_name = "orders"

urlpatterns = [
    path("window/order/", WindowOrderCreateAPIView.as_view(), name="order-window"),
]
