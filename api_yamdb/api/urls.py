from django.urls import include, path
from rest_framework import routers

from .views import (
    CommentViewSet,
    ReviewViewSet,
    TitleViewSet,
    CategoryViewSet,
    GenreViewSet
)

router_v1 = routers.DefaultRouter()
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router_v1.register(
    'titles',
    TitleViewSet,
    basename='titles'
)
<<<<<<< HEAD
router_v1.register(
=======
router.register(
>>>>>>> 8592dfa055ba42d0b72019126da191d6261c5f7e
    'categories',
    CategoryViewSet,
    basename='Category'
)
<<<<<<< HEAD

router_v1.register(
    'genres',
    GenreViewSet,
    basename='Genre'
)
=======
>>>>>>> 8592dfa055ba42d0b72019126da191d6261c5f7e

router.register(
    'genres',
    GenreViewSet,
    basename='Genre'
)

router. register()
urlpatterns = [
    path('v1/', include(router_v1.urls)),
]
