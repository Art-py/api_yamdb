from django.db import models
from django.contrib.auth.models import AbstractUser


class CreateDate(models.Model):
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        abstract = True


class User(AbstractUser):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    ROLE_CHOICES = [
        (USER, 'User'),
        (MODERATOR, 'Moderator'),
        (ADMIN, 'Admin'),
    ]
    bio = models.TextField(
        'Биография',
        blank=True
    )
    role = models.CharField(max_length=9, choices=ROLE_CHOICES, default=USER)


class Category(models.Model):
    """Категории: фильмы, книги, музыка и т.д."""
    name = models.CharField(
        max_length=256,
        unique=True,
        verbose_name='Категория',
        help_text='Укажите категорию'
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name='Слаг'
    )

    def __str__(self):
        return self.slug


class Genre(models.Model):
    """Жанры произведений"""
    name = models.CharField(
        max_length=256,
        unique=True,
        verbose_name='Жанр',
        help_text='Укажите жанр'
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name='Слаг'
    )

    def __str__(self):
        return self.slug


class Title(models.Model):
    name = models.TextField()
    year = models.IntegerField()
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        null=True
    )
    genre = models.ManyToManyField(Genre)


class Review(CreateDate):
    """Текстовые отзывы к произведениям."""
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    score = models.IntegerField()
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews'
    )


class Comment(CreateDate):
    """Комментарии к отзывам."""
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    