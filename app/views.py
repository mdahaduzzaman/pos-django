from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from drf_spectacular.utils import extend_schema
from drf_spectacular.types import OpenApiTypes

from app.models import InventoryTransaction, PurchaseOrder, PurchaseOrderItem
from app.permissions import IsManager
from app.serializers import PurchaseOrderSerializer, ReceiveItemSerializer
from app.choices import StatusChoices, TransactionTypeChoices


@extend_schema(tags=["purchase-orders"])
class PurchaseOrderViewSet(ModelViewSet):
    queryset = PurchaseOrder.objects.all().order_by("-created_at")
    serializer_class = PurchaseOrderSerializer
    filterset_fields = ["status"]
    http_method_names = ["get", "post", "delete"]

    def get_object(self) -> PurchaseOrder:
        return super().get_object()

    @extend_schema(
        request=None,
        responses={
            200: OpenApiTypes.OBJECT,
        },
    )
    @action(detail=True, methods=["post"], permission_classes=[IsManager])
    def approve(self, request, pk=None):
        purchase_order = self.get_object()
        purchase_order.status = StatusChoices.APPROVED
        purchase_order.save()
        return Response({"detail": "approved successfully"}, status=status.HTTP_200_OK)

    @extend_schema(
        request=ReceiveItemSerializer(many=True),
        responses={
            200: OpenApiTypes.OBJECT,
        },
    )
    @action(detail=True, methods=["post"])
    def receive(self, request, pk=None):
        purchase_order = self.get_object()
        if purchase_order.status not in [
            StatusChoices.APPROVED,
            StatusChoices.PARTIALLY_DELIVERED,
        ]:
            raise PermissionDenied("Only approved purchase orders can be received")

        serializer = ReceiveItemSerializer(
            data=request.data, many=True, context={"purchase_order": purchase_order}
        )
        serializer.is_valid(raise_exception=True)

        # flag to check all line items are received
        is_received_all = True
        for data in serializer.validated_data:
            item: PurchaseOrderItem = data["item"]
            previous_quantity = item.received_quantity

            # updating received quantity
            item.received_quantity += data["quantity"]
            item.save(update_fields=["received_quantity"])

            # updating the product stock
            product = item.product
            product.current_stock += data["quantity"]
            product.save(update_fields=["current_stock"])

            # if received_quantity and required quantity aren't same then mark as incomplete
            if item.received_quantity != item.quantity:
                is_received_all = False

            # Log inventory transaction
            InventoryTransaction.objects.create(
                product=item.product,
                transaction_type=(
                    TransactionTypeChoices.COMPLETELY_RECEIVED
                    if item.quantity == item.received_quantity
                    else TransactionTypeChoices.PARTIALLY_RECEIVED
                ),
                previous_qunatity=previous_quantity,
                updated_quantity=item.received_quantity,
                note=f"Received {data["quantity"]} item",
            )
        if is_received_all:
            # update the po status as completed when all items are received
            purchase_order.status = StatusChoices.COMPLETED
            purchase_order.save(update_fields=["status"])
        else:
            # update the po status as partially delivered
            if purchase_order.status != StatusChoices.PARTIALLY_DELIVERED:
                purchase_order.status = StatusChoices.PARTIALLY_DELIVERED
                purchase_order.save(update_fields=["status"])

        return Response(
            {"detail": "Items received successfully."}, status=status.HTTP_200_OK
        )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.status != StatusChoices.PENDING:
            raise PermissionDenied("Only pending purchase orders can be deleted.")
        return super().destroy(request, *args, **kwargs)
