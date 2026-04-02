"""
URL configuration for food_delivery project.
"""
from django.http import HttpResponse, JsonResponse
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Food Delivery API",
        default_version='v1',
        description="API documentation for Food Delivery Application",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@fooddelivery.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # Homepage - Welcome message
    path('', lambda request: JsonResponse({
        'message': 'Welcome to Food Delivery API!',
        'status': 'running',
        'version': '1.0.0',
        'docs': '/api/docs/',
        'redoc': '/api/redoc/',
        'frontend': 'http://localhost:3001'
    })),
    
    # API Documentation
    path('api/docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
    # API endpoints
    path('api/auth/', include('apps.authentication.urls')),
    path('api/', include('apps.food.urls')),
    path('api/', include('apps.cart.urls')),
    path('api/', include('apps.orders.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
