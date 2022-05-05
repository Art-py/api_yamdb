from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import serializers

from .validators import UsernameValidator
from reviews.models import Category, Genre, Comment, Title, Review

User = get_user_model()


class SignupUserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150, validators=[UsernameValidator()])
    email = serializers.EmailField(max_length=254)


class TokenRequestSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150, validators=[UsernameValidator()])
    confirmation_code = serializers.CharField(
        max_length=settings.CONFIRMATION_CODE_LENGTH
    )


class FullUserSerializer(serializers.ModelSerializer):
    """Сериализатор для выполнения операций пользователями с ролью ADMIN."""
    class Meta():
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
        if Review.objects.filter(
                author=self.context.get('request').user.id,
                title=self.context['view'].kwargs.get('title_id')
        ).exists():
            raise serializers.ValidationError(
                'Нельзя писать второй отзыв!'
            )
        return data


class ReadTitlesSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)

    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = ('__all__')


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
