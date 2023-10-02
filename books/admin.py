from ckeditor.widgets import CKEditorWidget
from django import forms
from django.contrib import admin

from .models import Genre, Book, Author, Rating, Review


class BookAdminForm(forms.ModelForm):
    """Форма с виджетом ckeditor"""
    description = forms.CharField(label="Описание", widget=CKEditorWidget())

    class Meta:
        model = Book
        fields = '__all__'


class ReviewInline(admin.TabularInline):
    """Отзывы на странице книги"""
    model = Review
    extra = 1


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """Книги"""
    list_display = ("name", "slug", "is_active")
    search_fields = ("name",)
    inlines = [ReviewInline]
    save_on_top = True
    save_as = True
    list_editable = ("is_active",)
    form = BookAdminForm
    fieldsets = (
        (None, {
            "fields": (("name",),)
        }),
        (None, {
            "fields": ("description",)
        }),
        (None, {
            "fields": (("published_date", ),)
        }),
        (None, {
            "fields": (("authors", "genres"),)
        }),
        ("Options", {
            "fields": (("slug", "is_active"),)
        }),
    )


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Отзывы к фильму"""
    list_display = ("user", "book", "id")


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """Жанры"""
    list_display = ("name", "slug")


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    """Актеры"""
    list_display = ("name",)


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    """Рейтинг"""
    list_display = ("star", "book", "user")


admin.site.site_title = "Books app"
admin.site.site_header = "Books app"
