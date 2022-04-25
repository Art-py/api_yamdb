from django.db import models
from django.contrib.auth import get_user_model

##### По заданию должна быть другая модель!!!!
### Изменить модель после получения новой от Артема!!!!!!
User = get_user_model()


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