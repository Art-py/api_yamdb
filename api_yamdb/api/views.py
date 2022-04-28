from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets, mixins
from rest_framework import permissions
from rest_framework.decorators import api_view
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from .serializers import CommentSerializer, ReviewSerializer, CategorySerializer, GenreSerializer, SimpleUserSerializer, TokenRequestSerializer, FullUserSerializer
from .permissions import IsAuthor, IsReadOnly, IsAdmin, IsModerator
from reviews.models import Category, Genre, Comment, Review, Title
from .utils import generate_confirmation_code

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
        username=serializer.validated_data['username'],
        confirmation_code=serializer.validated_data['confirmation_code']
    )
    token = AccessToken.for_user(user)
    return Response({'token': str(token)})


class UserViewSet(viewsets.ModelViewSet):
    model = User
    serializer_class = FullUserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAdmin]


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
    pass


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
