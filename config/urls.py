from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from rest_framework import routers
from api import views
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from api.views import UserRegistrationView, UserView, BuyerProfileUpdateView, SellerProfileUpdateView
from rest_framework_simplejwt.views import (
   TokenObtainPairView,
   TokenRefreshView,
)

# Set up the API router
api_router = routers.DefaultRouter()
api_router.register(r'best-practices', views.BestPracticeViewSet)
api_router.register(r'competitions', views.CompetitionViewSet)
api_router.register(r'certifications', views.CertificationViewSet)
api_router.register(r'olive-varieties', views.OliveVarietyViewSet)
api_router.register(r'buyers', views.BuyerViewSet)
api_router.register(r'products', views.ProductViewSet)
api_router.register(r'orders', views.OrderViewSet)
api_router.register(r'sellers', views.SellerViewSet)


urlpatterns = [
   path('', RedirectView.as_view(url='/api/schema/swagger/', permanent=False)),
   path('admin/', admin.site.urls),
   path('api/', include(api_router.urls)),  # Include the API router URLs
   path('api/schema/', SpectacularAPIView.as_view(), name='schema'),  # Schema endpoint
   path('api/schema/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),  # Swagger UI
   path('api/users/register/', UserRegistrationView.as_view(), name='register'),
   path('api/users/login/', TokenObtainPairView.as_view(), name='login'),
   path('api/users/login/refresh/', TokenRefreshView.as_view(), name='login_refresh'),
   path('api/users/me/', UserView.as_view(), name="user_details"),
   path('api/buyers/me/', BuyerProfileUpdateView.as_view(), name="buyer_details"),
   path('api/sellers/me/', SellerProfileUpdateView.as_view(), name="seller_details"),
    path('api/verify/<uuid:token_value>/', views.verify, name='verify')


]