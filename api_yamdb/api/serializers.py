from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from reviews.models import Category, Genre,  Comment

User = get_user_model()


class SimpleUserSerializer(serializers.ModelSerializer):
    """Сериализатор с username и email, используется для регистрации"""
    class Meta:
        model = User
        fields = [
            'username',
            'email',
        ]
        extra_kwargs = {
            'email': {
                'required': True,
                'validators': [UniqueValidator(queryset=User.objects.all())],
            },
        }


class BasicUserSerializer(SimpleUserSerializer):
    """Сериализатор для пользователей с ролью не равной ADMIN."""
    class Meta(SimpleUserSerializer.Meta):
        fields = SimpleUserSerializer.Meta.fields + [
            'first_name',
            'last_name',
            'bio',
            'role',
        ]
        read_only_fields = ['role']


class FullUserSerializer(SimpleUserSerializer):
    """Сериализатор для пользователей с ролью ADMIN."""
    class Meta(BasicUserSerializer.Meta):
        read_only_fields = BasicUserSerializer.Meta.read_only_fields[:]
        read_only_fields.remove('role')


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для категорий"""
    class Meta:
        model = Category
        exclude = ('id',)


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для жанров"""
    class Meta:
        model = Genre
        exclude = ('id',)


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Comment


class ReviewSerializer(serializers.ModelSerializer):
    pass

