from rest_framework import permissions


class IsModerator(permissions.BasePermission):
    """Проверяет, является ли пользователь модератором"""
    
    def has_permission(self, request, view):
        # Проверяем, авторизован ли пользователь
        if not request.user.is_authenticated:
            return False
        
        # Проверяем, состоит ли пользователь в группе модераторов
        return request.user.groups.filter(name='moderators').exists()


class IsOwner(permissions.BasePermission):
    """Проверяет, является ли пользователь владельцем объекта"""
    
    def has_object_permission(self, request, view, obj):
        # Если пользователь - модератор, разрешаем доступ
        if request.user.groups.filter(name='moderators').exists():
            return True
        # Если у объекта нет владельца, разрешаем доступ всем авторизованным
        if not hasattr(obj, 'owner') or obj.owner is None:
            return request.user.is_authenticated
        
        # Проверяем, является ли пользователь владельцем объекта
        return obj.owner == request.user


class IsCourseOwner(permissions.BasePermission):
    """Проверяет, является ли пользователь владельцем курса"""
    
    def has_object_permission(self, request, view, obj):
        # Если пользователь - модератор, разрешаем доступ
        if request.user.groups.filter(name='moderators').exists():
            return True
        
        # Если у курса нет владельца, разрешаем доступ всем авторизованным
        if obj.owner is None:
            return request.user.is_authenticated
        
        # Проверяем, является ли пользователь владельцем курса
        return obj.owner == request.user


class IsLessonOwner(permissions.BasePermission):
    """Проверяет, является ли пользователь владельцем урока"""
    
    def has_object_permission(self, request, view, obj):
        # Если пользователь - модератор, разрешаем доступ
        if request.user.groups.filter(name='moderators').exists():
            return True
        # Если у урока нет владельца, разрешаем доступ всем авторизованным
        if obj.owner is None:
            return request.user.is_authenticated
        
        # Проверяем, является ли пользователь владельцем урока
        return obj.owner == request.user
