from typing import List
from rest_framework import serializers
from django.db import transaction
from django.contrib.auth.models import User

from app.models import PurchaseOrder, PurchaseOrderItem


class PurchaseOrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrderItem
        exclude = ["received_quantity", "purchase_order", "created_at", "updated_at"]


class PurchaseOrderSerializer(serializers.ModelSerializer):
    items = PurchaseOrderItemSerializer(many=True)

    class Meta:
        model = PurchaseOrder
        exclude = ["created_by_id", "created_by_username", "created_at", "updated_at"]
        read_only_fields = ["status"]

    @transaction.atomic
    def create(self, validated_data: dict):
        items_data: List[dict] = validated_data.pop("items", [])

        # Get the user from the request context
        user: User = self.context["request"].user

        # Create the PO with created by
        po = PurchaseOrder.objects.create(
            **validated_data, created_by_id=user.pk, created_by_username=user.username
        )

        # Build PurchaseOrderItem instances
        items = [
            PurchaseOrderItem(purchase_order=po, **item_data)
            for item_data in items_data
        ]

        # Bulk create
        PurchaseOrderItem.objects.bulk_create(items)

        return po


class ReceiveItemSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    quantity = serializers.IntegerField()

    def validate(self, data):
        po: PurchaseOrder = self.context["purchase_order"]

        if not isinstance(po, PurchaseOrder):
            raise serializers.ValidationError("Purchase order not found")

        # getting the object using related manager
        item: PurchaseOrderItem = po.items.filter(id=data["id"]).first()

        if not item:
            raise serializers.ValidationError({"id": "Item not found in this Purchase Order."})

        # checking more than items are passed
        if item.received_quantity + data["quantity"] > item.quantity:
            raise serializers.ValidationError(
                {
                    "quantity": f"{item.quantity - item.received_quantity} needed. But given {data["quantity"]}."
                }
            )

        data["item"] = item  # pass item instance for later use
        return data
