from rest_framework import serializers

from reviews.models import Comment, Title


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


class TitlesSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Title
