"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Travel API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('admin/', admin.site.urls),
    path('api/', include('accounts.urls')),
    path('api/', include('core.urls')),
]

urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
#  {
#     "card_number": "4242424242424242",  
#     "expiry_month": "12",  
#     "expiry_year": "2025", 
#     "cvc": "123"
# }


# {
#     "username": "mohammad",
#     "tokens": {
#         "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcxODg5ODYyMywiaWF0IjoxNzE4MDM0NjIzLCJqdGkiOiJiMGFmN2ExNzE3MjU0NDYxODAzZmVlNWQ2YTkxMTI1NSIsInVzZXJfaWQiOjF9.Og-6vq8cFAqgX0jZ9idZ0AAw1bQmDhI5-Q_hkekfB1k",
#         "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzE4MTIxMDIzLCJpYXQiOjE3MTgwMzQ2MjMsImp0aSI6ImYzYTUxZTYwZDcwMjQ4NDFiYWFjYWIyNDk3Mjg3NjM0IiwidXNlcl9pZCI6MX0.dAO1tFGQ04KzTmVNVCjgSo4_Okvqg6w1VnDR8TGq86E"
#     }
# }