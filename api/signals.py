from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from .models import Product

@receiver(post_migrate)
def create_permissions_and_groups(sender, **kwargs):
    if sender.name == 'api':  # Ensure this runs only for your app
        # Create permissions
        content_type = ContentType.objects.get_for_model(Product)

        can_add_product, _ = Permission.objects.get_or_create(
            codename='can_add_product',
            name='Can add product',
            content_type=content_type,
        )

        can_view_product, _ = Permission.objects.get_or_create(
            codename='can_view_product',
            name='Can view product',
            content_type=content_type,
        )

        # Create groups
        buyer_group, _ = Group.objects.get_or_create(name='Buyers')
        producer_group, _ = Group.objects.get_or_create(name='Producers')

        # Assign permissions to groups
        buyer_group.permissions.add(can_view_product)  # Buyers can view products
        producer_group.permissions.add(can_add_product)  # Producers can add products
        producer_group.permissions.add(can_view_product)  # Producers can also view products