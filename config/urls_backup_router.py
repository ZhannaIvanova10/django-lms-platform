from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from users.views import UserProfileView, PaymentListView
from materials.views import (
    CourseViewSet, 
    LessonCreateAPIView, 
    LessonListAPIView, 
    LessonRetrieveAPIView, 
    LessonUpdateAPIView, 
    LessonDestroyAPIView,
    SubscriptionAPIView
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register(r'courses', CourseViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    # Уроки
    path('api/lessons/create/', LessonCreateAPIView.as_view(), name='lesson-create'),
    path('api/lessons/', LessonListAPIView.as_view(), name='lesson-list'),
    path('api/lessons/<int:pk>/', LessonRetrieveAPIView.as_view(), name='lesson-retrieve'),
    path('api/lessons/<int:pk>/update/', LessonUpdateAPIView.as_view(), name='lesson-update'),
    path('api/lessons/<int:pk>/delete/', LessonDestroyAPIView.as_view(), name='lesson-destroy'),
    
    # Подписки
    path('api/subscriptions/', SubscriptionAPIView.as_view(), name='subscriptions'),
    
    # Аутентификация
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Пользователи
    path('api/users/profile/', UserProfileView.as_view(), name='user-profile'),
    path('api/payments/', PaymentListView.as_view(), name='payment-list'),
]
