from django.contrib import admin

from app.models import (
    Supplier,
    Product,
    PurchaseOrder,
    PurchaseOrderItem,
    InventoryTransaction,
)


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ["name", "contact_email", "phone"]
    readonly_fields = ["id", "created_at", "updated_at"]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["sku", "name", "unit_price", "current_stock", "reorder_threshold"]
    readonly_fields = ["id", "created_at", "updated_at"]


@admin.register(PurchaseOrder)
class PurchaseOrderAdmin(admin.ModelAdmin):
    list_display = ["supplier", "order_date", "status"]
    readonly_fields = ["id", "created_at", "updated_at"]


@admin.register(PurchaseOrderItem)
class PurchaseOrderItemAdmin(admin.ModelAdmin):
    list_display = ["product", "quantity", "unit_price", "received_quantity"]
    readonly_fields = ["id", "created_at", "updated_at"]


@admin.register(InventoryTransaction)
class InventoryTransactionAdmin(admin.ModelAdmin):
    list_display = [
        "product",
        "transaction_type",
        "previous_qunatity",
        "updated_quantity",
    ]
    readonly_fields = ["id", "created_at", "updated_at"]
