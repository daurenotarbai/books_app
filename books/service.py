from django_filters import rest_framework as filters
from rest_framework.pagination import PageNumberPagination

from .models import Book


class PaginationBook(PageNumberPagination):
    page_size = 2
    max_page_size = 1000


class CharFilterInFilter(filters.BaseInFilter, filters.CharFilter):
    pass


class BookFilter(filters.FilterSet):
    genres = CharFilterInFilter(field_name='genres__name', lookup_expr='in')
    authors = CharFilterInFilter(field_name='authors__name', lookup_expr='in')
    published_date = filters.DateFromToRangeFilter()

    class Meta:
        model = Book
        fields = ['genres', 'authors', 'published_date']
