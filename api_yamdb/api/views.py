from django.shortcuts import get_object_or_404
from rest_framework import filters, viewsets, mixins
from rest_framework import permissions
from rest_framework.pagination import LimitOffsetPagination

from reviews.models import Comment, Review
from .serializers import CommentSerializer
from .permissions import IsAuthor, IsReadOnly, IsAdmin, IsModerator


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsAuthor, IsAdmin, IsModerator, IsReadOnly,)

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        return review.comments.filter(review=review)


class ReviewViewSet(viewsets.ModelViewSet):
    pass


class TitleViewSet(viewsets.ModelViewSet):
    pass