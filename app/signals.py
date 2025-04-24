from django.dispatch import receiver
from django.db.models.signals import post_save, post_migrate
from django.contrib.auth.models import Group

from app.models import Product


@receiver(post_save, sender=Product)
def calculate_load_mileage_and_save(sender, instance: Product, created: bool, **kwargs):
    if instance.current_stock < instance.reorder_threshold:
        print("Reorder Needed")


@receiver(post_migrate)
def schedule_audit_logs(sender, **kwargs):
    if sender.name == "app":
        groups = ["manager"]
        for group in groups:
            Group.objects.get_or_create(name=group)
