from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter

from materials.views import CourseViewSet, LessonListCreateView, LessonRetrieveUpdateDestroyView
from lms.views import PaymentViewSet
from users.views import UserCreateView, UserProfileView, UserViewSet

router = DefaultRouter()
router.register(r'courses', CourseViewSet)
router.register(r'payments', PaymentViewSet)
router.register(r'users', UserViewSet)  # Для дополнительного задания

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    
    # Уроки через Generic классы
    path('api/lessons/', LessonListCreateView.as_view(), name='lesson-list-create'),
    path('api/lessons/<int:pk>/', LessonRetrieveUpdateDestroyView.as_view(), name='lesson-detail'),
    
    # Пользователи
    path('api/register/', UserCreateView.as_view(), name='register'),
    path('api/profile/', UserProfileView.as_view(), name='profile'),
    
    # REST Framework auth
    path('api/auth/', include('rest_framework.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
