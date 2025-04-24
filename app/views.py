from django.shortcuts import render

from app.models import PurchaseOrder
from app.choices import StatusChoices
from app.utils import generate_jwt_for_user


def index(request):
    pending_orders = PurchaseOrder.objects.prefetch_related("items").filter(
        status=StatusChoices.PENDING
    )
    completed_orders = PurchaseOrder.objects.filter(status=StatusChoices.COMPLETED)

    context = {
        "pending_orders": pending_orders,
        "completed_orders": completed_orders,
        "token": generate_jwt_for_user(request.user),
    }

    return render(request, "app/index.html", context=context)
