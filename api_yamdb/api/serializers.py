import datetime as dt

from rest_framework import serializers

from reviews.models import Category, Genre, Comment, Title, Review


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
