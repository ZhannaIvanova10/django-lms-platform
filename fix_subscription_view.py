import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Читаем текущий файл
with open('materials/views.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Находим и исправляем класс SubscriptionAPIView
import re

# Ищем текущий класс
pattern = r'class SubscriptionAPIView\(APIView\):(.*?)(?=\n\nclass|\Z)'
match = re.search(pattern, content, re.DOTALL)

if match:
    print("Найден SubscriptionAPIView")
    print("Текущий код:")
    print(match.group(0)[:500] + "...")
    
    # Заменяем на исправленную версию
    fixed_view = '''class SubscriptionAPIView(APIView):
    """
    APIView для управления подписками на курсы
    """
    permission_classes = [IsAuthenticated]
    serializer_class = SubscriptionSerializer

    def get(self, request, *args, **kwargs):
        """Получение списка подписок пользователя"""
        subscriptions = Subscription.objects.filter(user=request.user)
        serializer = self.serializer_class(subscriptions, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        """Создание или удаление подписки"""
        user = request.user
        course_id = request.data.get('course_id')

        if not course_id:
            return Response(
                {"error": "course_id обязателен"},
                status=status.HTTP_400_BAD_REQUEST
            )

        course_item = get_object_or_404(Course, id=course_id)

        # Проверяем, есть ли уже подписка
        subs_item = Subscription.objects.filter(
            user=user,
            course=course_item
        )

        # Если подписка есть - удаляем ее
        if subs_item.exists():
            subs_item.delete()
            message = 'Подписка удалена'
            is_subscribed = False
        # Если подписки нет - создаем ее
        else:
            Subscription.objects.create(user=user, course=course_item)
            message = 'Подписка создана'
            is_subscribed = True

        return Response({
            "message": message,
            "is_subscribed": is_subscribed,
            "course_id": course_id
        })'''
    
    # Заменяем в содержимом
    new_content = content.replace(match.group(0), fixed_view)
    
    with open('materials/views.py', 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print("\n✅ SubscriptionAPIView исправлен!")
else:
    print("SubscriptionAPIView не найден")
