from django.urls import include, path
from rest_framework import routers

from .views import (
    signup,
    token,
    UserViewSet,
    CommentViewSet,
    ReviewViewSet,
    TitleViewSet,
    CategoryViewSet,
    GenreViewSet
)

router_v1 = routers.DefaultRouter()
router_v1.register(
    'users',
    UserViewSet,
    basename='users'
)
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
router_v1.register('titles', TitleViewSet, basename='titles')

router_v1.register(
    'categories',
    CategoryViewSet,
    basename='categories'
)

router_v1.register(
    'genres',
    GenreViewSet,
    basename='genres'
)

urlpatterns = [
    path('v1/auth/signup/', signup, name='signup'),
    path('v1/auth/token/', token, name='token'),
    path('v1/', include(router_v1.urls)),
]
