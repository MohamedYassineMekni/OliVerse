from rest_framework import serializers
from .models import BestPractice, Competition, Certification,  OliveVariety, Product, Buyer, Order, ProductImage, ProductVariation, Category,  Seller
from django.contrib.auth import get_user_model
User = get_user_model()

#Knowledge Hub Serializers
class BestPracticeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BestPractice
        fields = '__all__'


class CompetitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Competition
        fields = '__all__'


class CertificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certification
        fields = '__all__'

class OliveVarietySerializer(serializers.ModelSerializer):
    class Meta:
        model = OliveVariety
        fields = '__all__'


#Marketplace Serializers

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id','image']


class ProductVariationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariation
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    variations = ProductVariationSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    class Meta:
        model = Product
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
      class Meta:
          model = Order
          fields = '__all__'


#User Management Serializers
class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','email','password', 'user_type']
        extra_kwargs = {
        'password': {'write_only': True},
        }
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        if user.user_type == 'seller':
            Seller.objects.create(user=user)
        elif user.user_type == 'buyer':
            Buyer.objects.create(user=user)
        return user

class SellerSerializer(serializers.ModelSerializer):
   class Meta:
      model = Seller
      fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    buyer_profile = serializers.SerializerMethodField()
    seller_profile = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'user_type', 'buyer_profile','seller_profile']

    def get_buyer_profile(self, obj):
        if hasattr(obj, 'buyer'):
             buyer = obj.buyer
             return {
                 'id': buyer.id,
                 'address': buyer.address,
                  'favorite_products': [product.id for product in buyer.favorite_products.all()]
                }
        return None

    def get_seller_profile(self, obj):
        if hasattr(obj, 'seller'):
            seller = obj.seller
            return {
               'id': seller.id,
               'farm_location': seller.farm_location,
               'production_methods': seller.production_methods,
                'contact_details': seller.contact_details,
               'latitude': seller.latitude,
                'longitude': seller.longitude
              }
        return None


class BuyerSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Buyer
        fields = ['id','user', 'address', 'favorite_products']