import datetime as dt

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.validators import UniqueValidator, UniqueTogetherValidator

from reviews.models import Category, Genre, Comment, Title, Review

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
                'validators': [
                    UniqueValidator(
                        queryset=User.objects.all(),
                        message='A user with that email already exists.'
                    )
                ],
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


class TokenRequestSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()


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
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review
        # validators = [
        #     UniqueTogetherValidator(
        #         queryset=Review.objects.all(),
        #         fields=['author', 'score']
        #     )
        # ]

    def validate(self, data):
        title_id = self.context['view'].kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        if self.context.get('request').user == 
        self.context.get('request').parser_context.get('kwargs').get('title_id')

:
            raise serializers.ValidationError(
                'Нельзя подписаться на самого себя!'
            )
        return data



class TitlesSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        fields = ('id',
                  'name',
                  'year',
                  'rating',
                  'description',
                  'genre',
                  'category'
                  )
        model = Title

    def validate_year(self, value):
        year = dt.date.today().year
        if value > year:
            raise serializers.ValidationError(
                'Проверьте год выхода произведения!'
            )
        return value
