from django.db import models


class StatusChoices(models.TextChoices):
    PENDING = 'Pending', 'Pending'
    APPROVED = 'Approved', 'Approved'
    PARTIALLY_DELIVERED = 'Partially Delivered', 'Partially Delivered'
    COMPLETED = 'Completed', 'Completed'


class TransactionTypeChoices(models.TextChoices):
    PARTIALLY_RECEIVED = 'Partially Received', 'Partially Received'
    COMPLETELY_RECEIVED = 'Completely Received', 'Completely Received'
