import datetime as dt

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError


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
    confirmation_code = models.CharField(
        max_length=settings.CONFIRMATION_CODE_LENGTH,
        null=True
    )

    class Meta(AbstractUser.Meta):
        constraints = [
            models.CheckConstraint(
                check=~models.Q(username__iexact='me'),
                name='username_me_is_reserved'
            ),
        ]


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


def no_future_year(value):
    if value > dt.date.today().year:
        raise ValidationError(
            'Год выхода произведения не может быть больше текущего!'
        )


class Title(models.Model):
    """Произведения."""
    name = models.TextField(help_text='Наименование произведения')
    year = models.IntegerField(
        help_text='Год выхода произведения',
        validators=[no_future_year]
    )
    description = models.TextField(
        help_text='Описание произведения',
        blank=True
    )
    genre = models.ManyToManyField(Genre, help_text='Жанр произведения')
    category = models.ForeignKey(
        Category,
        help_text='Категория произведения',
        on_delete=models.SET_NULL,
        related_name='titles',
        null=True
    )


class ReviewAndCommentBase(models.Model):
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        abstract = True
        default_related_name = '%(model_name)s'
        ordering = ['-pub_date']


class Review(ReviewAndCommentBase):
    """Текстовые отзывы к произведениям."""

    score = models.IntegerField()
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_review'
            )
        ]


class Comment(ReviewAndCommentBase):
    """Комментарии к отзывам."""

    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments'
    )
