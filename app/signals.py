from django.dispatch import receiver
from django.db.models.signals import post_save

from app.models import Product


@receiver(post_save, sender=Product)
def calculate_load_mileage_and_save(sender, instance: Product, created: bool, **kwargs):
    if instance.current_stock < instance.reorder_threshold:
        print("Reorder Needed")
