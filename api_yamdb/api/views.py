from rest_framework import filters, viewsets, mixins
from django_filters.rest_framework import DjangoFilterBackend

from api.serializers import CategorySerializer, GenreSerializer
from reviews.models import Category, Genre


class CommentViewSet(viewsets.ModelViewSet):
    ...


class ReviewViewSet(viewsets.ModelViewSet):
    ...


class TitleViewSet(viewsets.ModelViewSet):
    ...


class CategoryViewSet(viewsets.ModelViewSet):
<<<<<<< HEAD
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
=======
    ...


class GenreViewSet(viewsets.ModelViewSet):
    ...
>>>>>>> 8592dfa055ba42d0b72019126da191d6261c5f7e
