from django.db import models
from django.contrib.auth.models import AbstractUser


ROLE = (
    ('user', 'USER'),
    ('moderator', 'MODERATOR'),
    ('admin', 'ADMIN')
)


class User(AbstractUser):
    bio = models.TextField(
        'Биография',
        blank=True
    )
    role = models.CharField(max_length=9, choices=ROLE, default='user')


class Review(models.Model):
    text = models.TextField()
    author = author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews'
    )
    score = models.IntegerField()
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)


class Comment(models.Model):
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments'
    )
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)


class Titles(models.Model):
    name = models.TextField()
    year = models.IntegerField()
