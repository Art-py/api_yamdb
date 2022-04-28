import datetime as dt

from rest_framework import serializers

from reviews.models import Category, Genre,  Comment, Title


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


class DictSerializer(serializers.Serializer):
    name = serializers.StringRelatedField(read_only=True)
    slug = serializers.StringRelatedField(read_only=True)


class TitlesSerializer(serializers.ModelSerializer):
    genre = DictSerializer(many=True, read_only=True)
    category = DictSerializer(read_only=True)

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
