from django.db import models
from django.db.models import Subquery
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, status, mixins, permissions
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Book, Author, Rating, Review, Genre, FavoriteBook
from .serializers import (
    BookListSerializer,
    BookDetailSerializer,
    ReviewStarCreateSerializer,
    AuthorListSerializer,
    AuthorDetailSerializer,
    ReviewSerializer,
    GenreListSerializer, FavoriteBookCreateSerializer,
)
from .service import BookFilter, PaginationBook


class BookViewSet(viewsets.ReadOnlyModelViewSet):
    """Вывод списка книг"""
    filter_backends = (DjangoFilterBackend,)
    filterset_class = BookFilter
    pagination_class = PaginationBook
    lookup_field = 'slug'

    def get_queryset(self):
        books = Book.objects.filter(is_active=True).annotate(
            middle_star=models.Sum(models.F('ratings__star')) / models.Count(models.F('ratings'))
        ).prefetch_related('authors', 'genres').order_by('name')
        return books

    def get_serializer_class(self):
        if self.action == 'list':
            return BookListSerializer
        elif self.action == "retrieve":
            return BookDetailSerializer

    @swagger_auto_schema(request_body=ReviewStarCreateSerializer)
    @action(methods=['post'], detail=True, url_path='review', url_name='add-review',
            permission_classes=(IsAuthenticated,))
    def add_review(self, request, slug=None):
        """Добавить отзыв"""
        data = request.data
        serializer = ReviewStarCreateSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        Rating.objects.update_or_create(
            user=request.user, book_id=data['book'],
            defaults={'star': data.pop('star')}
        )
        Review.objects.create(
            user=request.user, book_id=data['book'],
            text=data['text']
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(methods=['GET'], detail=True, url_path='reviews', url_name='get-review')
    def get_review(self, request, slug, *args, **kwargs):
        """Вывод списка отзывов"""
        books = Review.objects.filter(book__slug=slug)
        self.paginate_queryset(books)
        serializer = ReviewSerializer(books, many=True)
        return self.get_paginated_response(serializer.data)


class AuthorViewSet(viewsets.ReadOnlyModelViewSet):
    """Вывод авторов"""
    queryset = Author.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return AuthorListSerializer
        elif self.action == "retrieve":
            return AuthorDetailSerializer

    @action(methods=['GET'], detail=True, url_path='books', url_name='author-books')
    def get_books(self, request, pk, *args, **kwargs):
        """Вывод списка книг автора"""
        books = Book.objects.filter(authors__id=pk).annotate(
            middle_star=models.Sum(models.F('ratings__star')) / models.Count(models.F('ratings'))
        ).prefetch_related('authors', 'genres')
        self.paginate_queryset(books)
        serializer = BookListSerializer(books, many=True, context={'request': request})
        return self.get_paginated_response(serializer.data)


class GenreViewSet(viewsets.ReadOnlyModelViewSet):
    """Вывод жанров"""
    queryset = Genre.objects.all()
    serializer_class = GenreListSerializer
    lookup_field = 'slug'

    @action(methods=['GET'], detail=True, url_path='books', url_name='author-books')
    def get_books(self, request, slug, *args, **kwargs):
        """Вывод списка книг жанра"""
        books = Book.objects.filter(genres__slug=slug).annotate(
            middle_star=models.Sum(models.F('ratings__star')) / models.Count(models.F('ratings'))
        ).prefetch_related('authors', 'genres')
        self.paginate_queryset(books)
        serializer = BookListSerializer(books, many=True, context={'request': request})
        return self.get_paginated_response(serializer.data)


class FavoriteBookViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    queryset = Book.objects.all()
    serializer_class = FavoriteBookCreateSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_serializer_class(self):
        if self.action == 'list':
            return BookListSerializer
        elif self.action == "create":
            return FavoriteBookCreateSerializer

    def get_queryset(self):
        subquery = Subquery(
            FavoriteBook.objects.filter(user=self.request.user).values_list('book_id', flat=True)
        )
        books = Book.objects.filter(is_active=True, id__in=subquery).annotate(
            middle_star=models.Sum(models.F('ratings__star')) / models.Count(models.F('ratings'))
        ).prefetch_related('authors', 'genres').order_by('name')
        return books

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        FavoriteBook.objects.get_or_create(book_id=request.data['book'], user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
