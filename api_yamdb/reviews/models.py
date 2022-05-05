from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

from .validators import UsernameValidator, no_future_year


class User(AbstractUser):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    ROLE_CHOICES = [
        (USER, 'Пользователь'),
        (MODERATOR, 'Модератор'),
        (ADMIN, 'Администратор'),
    ]
    ROLE_MAX_LENGTH = max(len(role[0]) for role in ROLE_CHOICES)
    username = models.CharField(
        'Имя пользователя',
        max_length=150,
        unique=True,
        validators=[
            UsernameValidator()
        ]
    )
    email = models.EmailField('Электронная почта', unique=True, max_length=254)
    first_name = models.CharField('Имя', max_length=150, blank=True)
    last_name = models.CharField('Фамилия', max_length=150, blank=True)
    bio = models.TextField('Биография', blank=True)
    role = models.CharField(
        max_length=ROLE_MAX_LENGTH,
        choices=ROLE_CHOICES,
        default=USER
    )
    confirmation_code = models.CharField(
        max_length=settings.CONFIRMATION_CODE_LENGTH,
        null=True
    )

    @property
    def is_admin(self):
        return self.role == User.ADMIN or self.is_superuser or self.is_staff


class CategoryAndGenreBase(models.Model):
    name = models.CharField(
        max_length=256,
        unique=True,
        verbose_name='Название'
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name='Уникальный идентифиактор',
        help_text='Используйте буквы латиницы, цифры и символы "-" и "_"'
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class Category(CategoryAndGenreBase):
    """Категории: фильмы, книги, музыка и т.д."""
    class Meta(CategoryAndGenreBase.Meta):
        verbose_name = 'Категория произведения'
        verbose_name_plural = 'Категории произведений'


class Genre(CategoryAndGenreBase):
    """Жанры произведений"""
    class Meta(CategoryAndGenreBase.Meta):
        verbose_name = 'Жанр произведения'
        verbose_name_plural = 'Жанр произведений'


class Title(models.Model):
    """Произведения"""
    name = models.TextField(help_text='Наименование')
    year = models.IntegerField(
        help_text='Год выхода',
        validators=[no_future_year]
    )
    description = models.TextField(
        help_text='Описание',
        blank=True
    )
    genre = models.ManyToManyField(Genre, help_text='Жанр')
    category = models.ForeignKey(
        Category,
        help_text='Категория',
        on_delete=models.SET_NULL,
        related_name='titles',
        null=True
    )

    class Meta:
        ordering = ['name']


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
