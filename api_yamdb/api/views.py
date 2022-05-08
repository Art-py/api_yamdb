from django.conf import settings
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.db import IntegrityError
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Avg
from rest_framework import filters, viewsets
from rest_framework import permissions
from rest_framework.decorators import action, api_view
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
    ReadTitlesSerializer,
    UpdateTitlesSerializer,
    SignupUserSerializer,
    TokenRequestSerializer,
    ReviewCreateSerializer,
)
from .permissions import (
    IsReadOnlyOrIsAuthorOrIsAdminOrIsModerator,
    IsReadOnly,
    IsAdmin
)
from reviews.models import Category, Genre, Review, Title
from .utils import generate_confirmation_code
from .filters import TitleFilter

User = get_user_model()


@api_view(['POST'])
def signup(request):
    serializer = SignupUserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    try:
        user = User.objects.get_or_create(
            username=serializer.validated_data['username'],
            email=serializer.validated_data['email'],
        )[0]
    except IntegrityError:
        return Response(
            'Имя пользователя или электронная почта занята',
            status=400
        )
    user.confirmation_code = generate_confirmation_code(
        settings.CONFIRMATION_CODE_LENGTH
    )
    user.save()
    user.email_user(
        subject='Код подтверждения',
        message=user.confirmation_code
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
    if (user.confirmation_code
            != serializer.validated_data['confirmation_code']):
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
    permission_classes = (IsReadOnlyOrIsAuthorOrIsAdminOrIsModerator,)

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_review())

    def get_review(self):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        return review


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsReadOnlyOrIsAuthorOrIsAdminOrIsModerator,)

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())

    def get_title(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title

    def get_serializer_class(self):
        if self.action == 'create':
            return ReviewCreateSerializer
        return ReviewSerializer


class TitleViewSet(viewsets.ModelViewSet):
    permission_classes = (IsReadOnly | IsAdmin, )
    queryset = Title.objects.all().annotate(rating=Avg('reviews__score'))
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    ordering_fields = ['name', 'rating']

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ReadTitlesSerializer
        return UpdateTitlesSerializer


class CategoryViewSet(GenresCategoriesViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(GenresCategoriesViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
