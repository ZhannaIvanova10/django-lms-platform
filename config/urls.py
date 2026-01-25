from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from materials.views import CourseViewSet
from users.views import UserViewSet, UserProfileAPIView

# Создаем router для API
router = DefaultRouter()
router.register(r'courses', CourseViewSet)
# Уроки теперь обрабатываются отдельными APIView, а не ViewSet

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # API URLs
    path('api/', include(router.urls)),
    
    # JWT Authentication
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # User profile
    path('api/profile/', UserProfileAPIView.as_view(), name='user_profile'),
    
    # Materials app URLs (lessons, subscriptions)
    path('api/', include('materials.urls')),
    
    # Users app URLs
    path('api/', include('users.urls')),
]
