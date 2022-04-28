from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets, mixins
from rest_framework import permissions
from rest_framework.pagination import LimitOffsetPagination

from .serializers import (CommentSerializer,
                          ReviewSerializer,
                          CategorySerializer,
                          GenreSerializer,
                          TitlesSerializer)
from .permissions import IsAuthor, IsReadOnly, IsAdmin, IsModerator
from reviews.models import Category, Genre, Comment, Review, Title


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthor, IsAdmin, IsModerator, IsReadOnly,)

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        return review.comments.filter(review=review)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthor, IsAdmin, IsModerator, IsReadOnly,)

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.filter(title=title)


class TitleViewSet(viewsets.ModelViewSet):
    permission_classes = (IsReadOnly | IsAdmin, )
    queryset = Title.objects.all()
    serializer_class = TitlesSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('name', 'year', 'genre__slug', 'category__slug')


class CategoryViewSet(viewsets.ModelViewSet):
    #    permission_classes = (администратор или чтение)
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('=name',)
    lookup_field = 'slug'


class GenreViewSet(viewsets.ModelViewSet):
    #    permission_classes = (администратор или чтение)
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('=name',)
    lookup_field = 'slug'
