from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from django.urls import include, path

from .schema import swagger_urlpatterns


urlpatterns = [
    path("admin/", admin.site.urls),
    # path("", home, name="home"),
    # path("api/common/", include("apps.common.urls", namespace="common")),
    # path("api/accounts/", include("apps.accounts.urls", namespace="accounts")),
    # path("api/company/", include("apps.company.urls", namespace="company")),
    # path("api/materials/", include("apps.materials.urls", namespace="materials")),
    # path("api/orders/", include("apps.orders.urls", namespace="orders")),
]

urlpatterns += swagger_urlpatterns

if not settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


urlpatterns += [
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]