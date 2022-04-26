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


class Review(CreateDate):
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews'
    )
    score = models.IntegerField()


class Comment(CreateDate):
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments'
    )


class Titles(models.Model):
    name = models.TextField()
    year = models.IntegerField()
    category = models.ForeignKey(
        Сategories,
        on_delete=models.CASCADE,
        related_name='titles'
    )
