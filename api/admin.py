from django.contrib import admin
from .models import Buyer, Seller, Product, Order, BestPractice, Competition, Certification, OliveVariety, Category, ProductImage, ProductVariation, Email, VerificationToken, User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'email', 'first_name', 'last_name', 'user_type', 'is_active','is_staff','is_superuser', 'date_joined']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    list_filter = ['user_type','is_active']

@admin.register(Buyer)
class BuyerAdmin(admin.ModelAdmin):
    list_display = ['id','user', 'address']
    search_fields = ['user__username','address']

@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin):
    list_display = ['id','user', 'farm_location', 'production_methods', 'contact_details', 'latitude', 'longitude']
    search_fields = ['user__username', 'farm_location','contact_details']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'seller', 'name', 'description', 'price', 'stock', 'category']
    search_fields = ['name', 'description','seller__username']
    list_filter = ['category']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'buyer', 'order_date', 'order_status', 'product_name', 'product_price', 'quantity']
    search_fields = ['buyer__user__username','order_status', 'product_name']
    list_filter = ['order_status']

@admin.register(BestPractice)
class BestPracticeAdmin(admin.ModelAdmin):
    list_display = ['id','title', 'description', 'category', 'source_url', 'date_added']
    search_fields = ['title', 'description', 'category']
    list_filter = ['category']

@admin.register(Competition)
class CompetitionAdmin(admin.ModelAdmin):
    list_display = ['id','name', 'description', 'start_date', 'end_date', 'location', 'organizer', 'website_url']
    search_fields = ['name', 'description', 'location', 'organizer']

@admin.register(Certification)
class CertificationAdmin(admin.ModelAdmin):
    list_display = ['id','name', 'description', 'issuing_body', 'valid_period', 'cost', 'application_url']
    search_fields = ['name', 'description', 'issuing_body']

@admin.register(OliveVariety)
class OliveVarietyAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description', 'characteristics', 'region']
    search_fields = ['name', 'description', 'characteristics', 'region']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id','name']
    search_fields = ['name']


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'image']
    search_fields = ['product__name']

@admin.register(ProductVariation)
class ProductVariationAdmin(admin.ModelAdmin):
    list_display = ['id','product', 'size', 'price', 'packaging', 'harvest_year']
    search_fields = ['product__name', 'size', 'packaging']

@admin.register(Email)
class EmailAdmin(admin.ModelAdmin):
    list_display = ['id','subject', 'body', 'sender', 'recipient', 'status', 'created_at', 'updated_at', 'error_message']
    search_fields = ['subject', 'body', 'sender', 'recipient']
    list_filter = ['status']

@admin.register(VerificationToken)
class VerificationTokenAdmin(admin.ModelAdmin):
    list_display = ['id','user', 'token', 'created_at']
    search_fields = ['user__username', 'token']