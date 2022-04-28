from django.shortcuts import get_object_or_404
from rest_framework import filters, viewsets, mixins
from rest_framework import permissions
from rest_framework.pagination import LimitOffsetPagination

from reviews.models import Comment, Review, Title
from .serializers import CommentSerializer, ReviewSerializer, TitlesSerializer
from .permissions import IsAuthor, IsReadOnly, IsAdmin, IsModerator


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
    queryset = Title.objects.all()
    serializer_class = TitlesSerializer
    permission_classes = (IsAdmin, )
