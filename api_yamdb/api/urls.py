from django.urls import include, path
from rest_framework import routers

from .views import CommentViewSet, ReviewViewSet, TitleViewSet

router = routers.DefaultRouter()
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router.register(
    'titles',
    TitleViewSet,
    basename='titles'
)

urlpatterns = [
    path('', include(router.urls)),
]

