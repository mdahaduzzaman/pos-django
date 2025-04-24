from django.db import models
import uuid

from app.choices import StatusChoices, TransactionTypeChoices


class TimeStampedUUIDModel(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, unique=True, editable=False
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Supplier(TimeStampedUUIDModel):
    name = models.CharField(max_length=255)
    contact_email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True)
    address = models.TextField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "suppliers"


class Product(TimeStampedUUIDModel):
    sku = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    current_stock = models.PositiveIntegerField(default=0)
    reorder_threshold = models.PositiveIntegerField(default=10)  # Set threshold

    def __str__(self):
        return f"{self.name} ({self.sku})"

    class Meta:
        db_table = "products"


class PurchaseOrder(TimeStampedUUIDModel):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    order_date = models.DateField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=StatusChoices.choices,
        default=StatusChoices.PENDING,
        db_index=True,
    )
    notes = models.TextField(null=True, blank=True)

    # track who creates the PO
    created_by_id = models.BigIntegerField()
    created_by_username = models.CharField(max_length=150)

    def __str__(self):
        return f"{self.order_date} ({self.supplier.name})"

    class Meta:
        db_table = "purchase_orders"


class PurchaseOrderItem(TimeStampedUUIDModel):
    purchase_order = models.ForeignKey(
        PurchaseOrder, on_delete=models.CASCADE, related_name="items"
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    received_quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

    class Meta:
        db_table = "purchase_order_items"


class InventoryTransaction(TimeStampedUUIDModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    transaction_type = models.CharField(
        max_length=30, choices=TransactionTypeChoices.choices
    )
    previous_qunatity = models.IntegerField()
    updated_quantity = models.IntegerField()
    note = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = "inventory_transactions"
