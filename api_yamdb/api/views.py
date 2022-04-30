from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Avg
from rest_framework import filters, viewsets, mixins
from rest_framework import permissions
from rest_framework.decorators import action, api_view
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from .mixins import GenresCategoriesViewSet
from .serializers import (
    BasicUserSerializer,
    CategorySerializer,
    CommentSerializer,
    FullUserSerializer,
    GenreSerializer,
    ReviewSerializer,
    SimpleUserSerializer,
    TitlesSerializer,
    TokenRequestSerializer,
)
from .permissions import IsAuthor, IsReadOnly, IsAdmin, IsModerator
from reviews.models import Category, Genre, Review, Title
from .utils import generate_confirmation_code
from .filters import TitleFilter

User = get_user_model()


@api_view(['POST'])
def signup(request):
    # Возможно, пользователь был зарегистрирован администратором,
    # или хочет получить новый код
    # Поэтому пробуем найти его в базе.
    result = User.objects.filter(
        username=request.data.get('username'),
        email=request.data.get('email')
    )
    user = None
    if result.exists():
        user = result[0]
    serializer = SimpleUserSerializer(user, data=request.data)
    serializer.is_valid(raise_exception=True)
    confirmation_code = generate_confirmation_code()
    user = serializer.save(confirmation_code=confirmation_code)
    user.email_user(
        subject='Код подтверждения',
        message=confirmation_code
    )
    return Response(serializer.data, status=200)


@api_view(['POST'])
def token(request):
    serializer = TokenRequestSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(
        User,
        username=serializer.validated_data['username']
    )
    if user.confirmation_code != serializer.validated_data['confirmation_code']:
        return Response('Неверный код подтверждения', status=400)
    token = AccessToken.for_user(user)
    return Response({'token': str(token)})


class UserViewSet(viewsets.ModelViewSet):
    model = User
    serializer_class = FullUserSerializer
    queryset = User.objects.all()
    lookup_field = 'username'
    permission_classes = [IsAdmin]
    filter_backends = [filters.SearchFilter]
    search_fields = ['username']

    @action(
        methods=['GET', 'PATCH'],
        detail=False,
        url_path='me',
        permission_classes=[permissions.IsAuthenticated]
    )
    def me(self, request):
        if request.method == 'GET':
            return Response(BasicUserSerializer(request.user).data)
        serializer = BasicUserSerializer(
            request.user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsReadOnly | IsAuthor | IsAdmin | IsModerator,)

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        return review.comments.filter(review=review)

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsReadOnly | IsAuthor | IsAdmin | IsModerator,)

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.filter(title=title)

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class TitleViewSet(viewsets.ModelViewSet):
    permission_classes = (IsReadOnly | IsAdmin, )
    queryset = Title.objects.all().annotate(Avg("reviews__score"))
    serializer_class = TitlesSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter


class CategoryViewSet(GenresCategoriesViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(GenresCategoriesViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
