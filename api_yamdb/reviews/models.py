from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser


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


class Title(models.Model):
    """Произведения."""
    name = models.TextField()
    year = models.IntegerField()
    description = models.TextField(blank=True)
    rating = models.FloatField(null=True)
    genre = models.ManyToManyField(Genre)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        null=True
    )


class ReviewAndComment(models.Model):
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        abstract = True
        default_related_name = '%(model_name)s'


class Review(ReviewAndComment):
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


class Comment(ReviewAndComment):
    """Комментарии к отзывам."""

    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments'
    )
