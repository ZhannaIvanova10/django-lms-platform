from rest_framework.pagination import PageNumberPagination


class MaterialsPagination(PageNumberPagination):
    """
    Пагинатор для уроков и курсов
    """
    page_size = 10  # Количество элементов на странице по умолчанию
    page_size_query_param = 'page_size'  # Параметр для указания количества элементов на странице
    max_page_size = 100  # Максимальное количество элементов на странице
    
    def get_paginated_response(self, data):
        """
        Переопределяем ответ для добавления информации о пагинации
        """
        from rest_framework.response import Response
        
        return Response({
            'count': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'current_page': self.page.number,
            'total_pages': self.page.paginator.num_pages,
            'page_size': self.get_page_size(self.request),
            'results': data
        })

class SmallPagination(PageNumberPagination):
    """
    Пагинатор с небольшим количеством элементов
    """
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 20


class LargePagination(PageNumberPagination):
    """
    Пагинатор с большим количеством элементов
    """
    page_size = 25
    page_size_query_param = 'page_size'
    max_page_size = 50
