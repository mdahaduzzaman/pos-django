from django.urls import path, include
from rest_framework.routers import SimpleRouter

from app.views import PurchaseOrderViewSet

router = SimpleRouter()

router.register("purchase-orders", PurchaseOrderViewSet, basename="purchase-order")

urlpatterns = [
    path("", include(router.urls)),
]