from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter(trailing_slash=False)

router.register("books", views.BookViewSet, basename='books')
router.register('authors', views.AuthorViewSet, basename='authors')
router.register('genres', views.GenreViewSet, basename='genres')
router.register('favorites', views.FavoriteBookViewSet, basename='favorites')

urlpatterns = [
    path('', include(router.urls))
]
