from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.conf import settings
import uuid

class User(AbstractUser):
    USER_TYPES = (
        ('buyer', 'Buyer'),
        ('seller', 'Seller'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPES, default='buyer')

    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_set',
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_permissions_set',
        blank=True,
    )

    def __str__(self):
        return self.username

class Buyer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.TextField(blank=True, null=True)
    favorite_products = models.ManyToManyField('Product', related_name="favorited_by", blank=True)

    class Meta:
        app_label = 'api'

    def __str__(self):
        return self.user.username

class Seller(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    farm_location = models.CharField(max_length=200, blank=True, null=True)
    production_methods = models.TextField(blank=True, null=True)
    contact_details = models.TextField(blank=True, null=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=6, blank=True, null=True)

    class Meta:
        app_label = 'api'

    def __str__(self):
        return self.user.username

class Product(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE, null=True, limit_choices_to={'user_type': 'seller'})
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        app_label = 'api'
        permissions = [
            ("can_add_product", "Can add product"),
            ("can_view_product", "Can view product"),
        ]

    def __str__(self):
        return self.name

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.URLField()

    class Meta:
        app_label = 'api'

class ProductVariation(models.Model):
    product = models.ForeignKey(Product, related_name='variations', on_delete=models.CASCADE)
    size = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    packaging = models.CharField(max_length=100, blank=True, null=True)
    harvest_year = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        app_label = 'api'

    def __str__(self):
       return f"{self.product.name} - {self.size}"

class Order(models.Model):
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    order_status = models.CharField(max_length=20, choices=(
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ), default='pending')
    product_name = models.CharField(max_length=200, default='default product')
    product_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    quantity = models.IntegerField(default=1)

    class Meta:
        app_label = 'api'

    def __str__(self):
        return f"Order from {self.buyer}"

class BestPractice(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=100)
    source_url = models.URLField(blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'api'

    def __str__(self):
        return self.title

class Competition(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    location = models.CharField(max_length=200)
    organizer = models.CharField(max_length=200)
    website_url = models.URLField(blank=True, null=True)

    class Meta:
        app_label = 'api'

    def __str__(self):
        return self.name

class Certification(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    issuing_body = models.CharField(max_length=200)
    valid_period = models.CharField(max_length=100, blank=True, null=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    application_url = models.URLField(blank=True, null=True)

    class Meta:
        app_label = 'api'

    def __str__(self):
        return self.name

class OliveVariety(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    characteristics = models.TextField(blank=True, null=True)
    region = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        app_label = 'api'

    def __str__(self):
        return self.name
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        app_label = 'api'
        verbose_name_plural = 'Categories'

    def __str__(self):
      return self.name
class Email(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('sent', 'Sent'),
        ('failed', 'Failed'),
    ]
    subject = models.CharField(max_length=255)
    body = models.TextField()
    sender = models.EmailField(default=settings.DEFAULT_FROM_EMAIL)
    recipient = models.EmailField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    error_message = models.TextField(blank=True, null=True)


    def __str__(self):
        return f"{self.subject} to {self.recipient} - Status: {self.status}"

class VerificationToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.UUIDField(unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Token for {self.user.username}"