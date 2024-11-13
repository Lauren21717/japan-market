from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import OrderLineItem, Order

@receiver(post_save, sender=OrderLineItem)
def update_on_save(sender, instance, created, **kwargs):
    """
    Update order total on lineitem update/create
    """
    instance.order.update_total()


@receiver(post_delete, sender=OrderLineItem)
def update_on_delete(sender, instance, **kwargs):
    """
    Update order total on lineitem delete
    """
    instance.order.update_total()


@receiver(post_save, sender=Order)
def add_products_to_profile(sender, instance, created, **kwargs):
    """
    Add purchased products to the user's profile when an order is completed.
    """
    if created and instance.user_profile:
        profile = instance.user_profile
        order_line_items = OrderLineItem.objects.filter(order=instance)

        for item in order_line_items:
            profile.user_purchases.add(item.product)

        profile.save()
