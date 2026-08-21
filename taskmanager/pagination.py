from rest_framework.pagination import PageNumberPagination
from rest_framework.pagination import CursorPagination

class GlobalCursorPagination(CursorPagination):
    page_size = 6
    ordering = '-created_at'

class SubTaskPagination(PageNumberPagination):
    page_size = 5

