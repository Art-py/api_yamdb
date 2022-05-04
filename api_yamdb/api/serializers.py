from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

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

    def validate_username(self, value):
        if value.lower() == 'me':
            raise serializers.ValidationError('Username me is reserved.')
        return value


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
