"""
URL configuration for blog_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from blogs.views import UserViewSet, BlogViewSet
# from django.contrib import admin
# from rest_framework_simplejwt.views import TokenObtainPairView
# from rest_framework import permissions
# from drf_yasg.views import get_schema_view
# from drf_yasg import openapi

# schema_view = get_schema_view(
#     openapi.Info(
#         title="Blog API",
#         default_version='v1',
#         description="API for Blog application",
#         terms_of_service="https://www.google.com/policies/terms/",
#         contact=openapi.Contact(email="contact@blog.com"),
#         license=openapi.License(name="BSD License"),
#     ),
#     public=True,
#     permission_classes=[permissions.AllowAny],
# )

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'blogs', BlogViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    # path('admin/', admin.site.urls),
    # path('api/login/', TokenObtainPairView.as_view(), name='login'),
    # path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    # path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
