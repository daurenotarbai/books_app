from rest_framework import serializers

from users.models import User
from .models import Book, Review, Rating, Author, Genre, FavoriteBook


class FilterReviewListSerializer(serializers.ListSerializer):
    """Фильтр комментариев"""
    def to_representation(self, data):
        return super().to_representation(data)


class GenreListSerializer(serializers.ModelSerializer):
    """Вывод списка авторов"""
    class Meta:
        model = Genre
        fields = ('id', 'name', 'slug')


class AuthorListSerializer(serializers.ModelSerializer):
    """Вывод списка авторов"""
    class Meta:
        model = Author
        fields = ('id', 'name')


class AuthorDetailSerializer(serializers.ModelSerializer):
    """Вывод полного описани автора"""
    class Meta:
        model = Author
        exclude = ['changed_at', 'created_at']


class BookListSerializer(serializers.ModelSerializer):
    """Список книг"""
    authors = AuthorListSerializer(read_only=True, many=True)
    genres = serializers.SlugRelatedField(slug_field="name", read_only=True, many=True)
    middle_star = serializers.IntegerField()
    is_favorite = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = ("name", "middle_star", 'slug', 'authors', 'genres', 'is_favorite')

    def get_is_favorite(self, obj):
        user = self.context['request'].user
        if isinstance(user, User):
            return FavoriteBook.objects.filter(user=user, id=obj.id).exists()


class BookDetailSerializer(BookListSerializer):
    """Детальная страница книги"""
    authors = AuthorListSerializer(read_only=True, many=True)
    genres = serializers.SlugRelatedField(slug_field="name", read_only=True, many=True)

    class Meta:
        model = Book
        exclude = ['changed_at', 'created_at', 'is_active']


class ReviewStarCreateSerializer(serializers.Serializer):
    """Добавление отзыва с рейтингой"""
    text = serializers.CharField()
    book = serializers.IntegerField()
    star = serializers.IntegerField()

    @staticmethod
    def validate_star(star):
        if 1 > star or star > 10:
            raise serializers.ValidationError('invalid data')
        return star


class ReviewSerializer(serializers.ModelSerializer):
    """Вывод отзыво"""
    user = serializers.CharField()
    rating = serializers.SerializerMethodField()

    class Meta:
        list_serializer_class = FilterReviewListSerializer
        model = Review
        fields = ('id', 'user', 'text', 'rating')

    @staticmethod
    def get_rating(obj):
        rating = Rating.objects.get(user=obj.user, book=obj.book)
        return rating.star


class FavoriteBookCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteBook
        fields = ['book']