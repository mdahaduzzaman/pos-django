from django.urls import path, include
from rest_framework.routers import SimpleRouter

from app.api import PurchaseOrderViewSet
from app.views import index

router = SimpleRouter()

router.register("purchase-orders", PurchaseOrderViewSet, basename="purchase-order")

urlpatterns = [
    path("", index, name="index"),
    path("api/", include(router.urls)),
]