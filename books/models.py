from datetime import date

from django.db import models
from django.urls import reverse

from core.models import TimestampMixin
from users.models import User


class Author(TimestampMixin):
    """Авторы"""
    name = models.CharField("Имя", max_length=100)
    description = models.TextField("Описание")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('actor_detail', kwargs={"slug": self.name})

    class Meta:
        verbose_name = "Автор"
        verbose_name_plural = "Авторы"


class Genre(TimestampMixin):
    """Жанры"""
    name = models.CharField("Имя", max_length=100)
    slug = models.SlugField(max_length=160, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"


class Book(TimestampMixin):
    """Книга"""
    name = models.CharField("Название", max_length=100)
    description = models.TextField("Описание")
    authors = models.ManyToManyField(Author, verbose_name="Авторы", related_name="film_author")
    genres = models.ManyToManyField(Genre, verbose_name="Жанры")
    published_date = models.DateField("Дата публикации", default=date.today)
    slug = models.SlugField(max_length=130, unique=True)
    is_active = models.BooleanField("Активный", default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Книга"
        verbose_name_plural = "Книги"


class Rating(TimestampMixin):
    """Рейтинг"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings')
    star = models.PositiveSmallIntegerField(verbose_name="Звезда")
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        verbose_name="Книга",
        related_name="ratings"
    )

    def __str__(self):
        return f"{self.star} - {self.book}"

    class Meta:
        verbose_name = "Рейтинг"
        verbose_name_plural = "Рейтинги"
        unique_together = ['user', 'book']


class Review(TimestampMixin):
    """Отзывы"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField("Сообщение", max_length=5000)
    book = models.ForeignKey(
        Book,
        verbose_name="Книга",
        on_delete=models.CASCADE,
        related_name="reviews"
    )

    def __str__(self):
        return f"{self.user.email} - {self.book}"

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"


class FavoriteBook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.email} - {self.book}"

    class Meta:
        verbose_name = "Избранная"
        verbose_name_plural = "Избранные"
        unique_together = ['user', 'book']
