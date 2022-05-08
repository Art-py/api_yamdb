from django.conf import settings
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from reviews.validators import validate_username
from reviews.models import Category, Genre, Comment, Title, Review

User = get_user_model()


class UsernameSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=150,
        validators=[validate_username]
    )


class SignupUserSerializer(UsernameSerializer):
    email = serializers.EmailField(max_length=254)


class TokenRequestSerializer(UsernameSerializer):
    confirmation_code = serializers.CharField(
        max_length=settings.CONFIRMATION_CODE_LENGTH
    )


class FullUserSerializer(serializers.ModelSerializer):
    """Сериализатор для выполнения операций пользователями с ролью ADMIN."""
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        ]


class BasicUserSerializer(FullUserSerializer):
    """Сериализатор для выполнения операций пользователями с ролью не ADMIN."""
    class Meta(FullUserSerializer.Meta):
        read_only_fields = ['role']


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


class ReviewCreateSerializer(ReviewSerializer):

    def validate(self, data):
        title_id = self.context['view'].kwargs.get('title_id')
        author = self.context.get('request').user
        title = get_object_or_404(Title, id=title_id)
        if title.reviews.filter(author=author).exists():
            raise serializers.ValidationError(
                'Нельзя писать второй отзыв!'
            )
        return data


class ReadTitlesSerializer(serializers.ModelSerializer):

    genre = GenreSerializer(many=True)
    category = CategorySerializer()

    rating = serializers.IntegerField()

    class Meta:
        model = Title
        fields = ('id', 'name', 'year',
                  'rating', 'genre', 'category', 'description'
                  )
        read_only_fields = ['__all__']


class UpdateTitlesSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        many=True,
        slug_field='slug',
        queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )

    class Meta:
        model = Title
        fields = ('__all__')
