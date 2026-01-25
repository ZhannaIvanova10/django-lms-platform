from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def api_root(request):
    """Корневой endpoint с документацией API"""
    return Response({
        'message': 'LMS Platform API',
        'documentation': 'Используйте следующие endpoints:',
        'endpoints': {
            'admin_panel': '/admin/',
            'courses': '/api/courses/',
            'lessons': '/api/lessons/',
            'users': '/api/users/',
        },
        'instructions': {
            'courses': 'Используйте ViewSets (требование задания)',
            'lessons': 'Используйте Generic классы (требование задания)',
            'testing': 'Тестируйте через Postman или curl'
        }
    })

urlpatterns = [
    # Корневой URL
    path('', api_root, name='api-root'),
    
    # Админка
    path('admin/', admin.site.urls),
    
    # API
    path('api/', include('users.urls')),
    path('api/', include('materials.urls')),
]

# Медиа файлы для разработки
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
