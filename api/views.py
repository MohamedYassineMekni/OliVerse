from rest_framework import viewsets, generics, permissions
from .models import BestPractice, Competition, Certification, OliveVariety, Buyer, Product, Order, User, Seller, Email, VerificationToken
from api.serializers import BestPracticeSerializer, CompetitionSerializer, CertificationSerializer,  OliveVarietySerializer, BuyerSerializer, ProductSerializer, OrderSerializer, UserRegistrationSerializer, UserSerializer, SellerSerializer
from django_filters import rest_framework as filters
from django_filters import DateFromToRangeFilter, CharFilter
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
import csv
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.conf import settings
import uuid


class BestPracticeFilter(filters.FilterSet):
    date_added = DateFromToRangeFilter()
    title = CharFilter(field_name='title', lookup_expr='icontains')
    category = CharFilter(field_name='category', lookup_expr='iexact')

    class Meta:
        model = BestPractice
        fields = ['category', 'title', 'date_added']

class BestPracticeViewSet(viewsets.ModelViewSet):
    queryset = BestPractice.objects.all()
    serializer_class = BestPracticeSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = BestPracticeFilter

    @action(detail=False, methods=['get'])
    def search_by_keyword(self, request):
        keyword = request.query_params.get('keyword', None)

        if keyword:
            results = BestPractice.objects.filter(Q(title__icontains=keyword))
            serializer = self.get_serializer(results, many=True)
            return Response(serializer.data)
        else:
            return Response({'error': 'No keyword was provided'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def export_csv(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        response = Response(serializer.data, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="best_practices.csv"'

        writer = csv.DictWriter(response, fieldnames=list(serializer.child.fields))
        writer.writeheader()

        for row in serializer.data:
            writer.writerow(row)

        return response

class BuyerViewSet(viewsets.ModelViewSet):
    queryset = Buyer.objects.all()
    serializer_class = BuyerSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]  # Use IsAuthenticated

    def perform_create(self, serializer):
          product_id = self.request.data.get('product')
          print("Product ID:", product_id)
          if product_id is not None:
             try:
                product_id = int(product_id)
                product = Product.objects.get(id=product_id)
                print("Product object:", product)
                print("Product name:", product.name)
                print("Product price:", product.price)
             except ValueError:
                  raise NotFound(f"Invalid product id {product_id}, must be an integer")
             except Product.DoesNotExist:
                 raise NotFound(f"Product with id {product_id} was not found")
             serializer.save(
               buyer=self.request.user.buyer,
                  product_name=product.name,
                 product_price=product.price,
               )
          else:
                raise NotFound(f"Product id is required")

class CompetitionFilter(filters.FilterSet):
    name = CharFilter(field_name='name', lookup_expr='icontains')
    organizer = CharFilter(field_name='organizer', lookup_expr='icontains')
    location = CharFilter(field_name='location', lookup_expr='icontains')

    class Meta:
        model = Competition
        fields = ['name', 'organizer', 'location']

class CompetitionViewSet(viewsets.ModelViewSet):
    queryset = Competition.objects.all()
    serializer_class = CompetitionSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = CompetitionFilter

    @action(detail=False, methods=['get'])
    def search_by_keyword(self, request):
        keyword = request.query_params.get('keyword', None)

        if keyword:
            results = Competition.objects.filter(Q(name__icontains=keyword))
            serializer = self.get_serializer(results, many=True)
            return Response(serializer.data)
        else:
            return Response({'error': 'No keyword was provided'}, status=status.HTTP_400_BAD_REQUEST)

class CertificationFilter(filters.FilterSet):
    name = CharFilter(field_name='name', lookup_expr='icontains')
    issuing_body = CharFilter(field_name='issuing_body', lookup_expr='icontains')

    class Meta:
        model = Certification
        fields = ['name', 'issuing_body']

class CertificationViewSet(viewsets.ModelViewSet):
    queryset = Certification.objects.all()
    serializer_class = CertificationSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = CertificationFilter

    @action(detail=False, methods=['get'])
    def search_by_keyword(self, request):
        keyword = request.query_params.get('keyword', None)

        if keyword:
            results = Certification.objects.filter(Q(name__icontains=keyword))
            serializer = self.get_serializer(results, many=True)
            return Response(serializer.data)
        else:
            return Response({'error': 'No keyword was provided'}, status=status.HTTP_400_BAD_REQUEST)


class OliveVarietyFilter(filters.FilterSet):
    name = CharFilter(field_name='name', lookup_expr='icontains')
    region = CharFilter(field_name='region', lookup_expr='icontains')

    class Meta:
        model = OliveVariety
        fields = ['name', 'region']

class OliveVarietyViewSet(viewsets.ModelViewSet):
    queryset = OliveVariety.objects.all()
    serializer_class = OliveVarietySerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = OliveVarietyFilter

    @action(detail=False, methods=['get'])
    def search_by_keyword(self, request):
        keyword = request.query_params.get('keyword', None)

        if keyword:
            results = OliveVariety.objects.filter(Q(name__icontains=keyword))
            serializer = self.get_serializer(results, many=True)
            return Response(serializer.data)
        else:
            return Response({'error': 'No keyword was provided'}, status=status.HTTP_400_BAD_REQUEST)


from rest_framework import generics, permissions
from .serializers import UserRegistrationSerializer, UserSerializer
from rest_framework.response import Response
from rest_framework import status
class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.is_active = False  # Set user to inactive initially
            user.save()
            token_value = uuid.uuid4()
            token = VerificationToken.objects.create(user=user, token=token_value)
            # Create and send verification email
            verification_url = request.build_absolute_uri(f'/api/verify/{token_value}/')
            try:
                email_obj = Email.objects.create(
                    subject='Verify Your Account',
                    body=f'Please click the link to verify: {verification_url}',
                    recipient=user.email,
                    status='pending'
                )
                send_mail(
                    email_obj.subject,
                    email_obj.body,
                    settings.DEFAULT_FROM_EMAIL,
                    [email_obj.recipient],
                    fail_silently=False
                )
                email_obj.status = 'sent'
                email_obj.save()

            except Exception as e:
                email_obj.status = 'failed'
                email_obj.error_message = str(e)
                email_obj.save()
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserView(generics.RetrieveUpdateAPIView):
        serializer_class = UserSerializer
        permission_classes = [permissions.IsAuthenticated]
        def get_object(self):
            return self.request.user

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user_type = request.POST['user_type']  # 'buyer' or 'producer'

        user = User.objects.create_user(username=username, password=password, user_type=user_type)

        # Assign user to the appropriate group
        if user_type == 'buyer':
            buyer_group = Group.objects.get(name='Buyers')
            buyer_group.user_set.add(user)
        elif user_type == 'producer':
            producer_group = Group.objects.get(name='Producers')
            producer_group.user_set.add(user)

        return redirect('login')  # Redirect to login or another page
    return render(request, 'register.html')


def is_buyer(user):
    return user.groups.filter(name='Buyers').exists()

def is_producer(user):
    return user.groups.filter(name='Producers').exists()

@login_required
@user_passes_test(is_buyer)
@permission_required('api.can_view_product', raise_exception=True)
def view_products(request):
    # Logic for buyers to view products
    pass

@login_required
@user_passes_test(is_producer)
@permission_required('api.can_add_product', raise_exception=True)
def add_product(request):
    # Logic for producers to add products
    pass

# Create permissions for the Product model
content_type = ContentType.objects.get_for_model(Product)

Permission.objects.get_or_create(
    codename='can_add_product',
    name='Can add product',
    content_type=content_type,
)

Permission.objects.get_or_create(
    codename='can_view_product',
    name='Can view product',
    content_type=content_type,
)

def verify(request, token_value):
    try:
       token = VerificationToken.objects.get(token=token_value)
       user = token.user
       user.is_active = True
       user.save()
       token.delete()
       return render(request, 'home/success_verify.html', {'message': 'User verified successfully!'})
    except VerificationToken.DoesNotExist:
        return render(request, 'home/invalid_token.html', {'error': 'Invalid token!'})

class SellerViewSet(viewsets.ModelViewSet):
    queryset = Seller.objects.all()
    serializer_class = SellerSerializer

class BuyerProfileUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = BuyerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.buyer # Get the buyer profile that is associated to the user

class SellerProfileUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = SellerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.seller  # Get the seller profile that is associated to the user