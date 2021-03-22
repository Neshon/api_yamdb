from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from .views import GenreViewSet, CommentViewSet, CategoryViewSet, TitleViewSet, \
    ReviewViewSet, UserViewSet, TokenViewSet, AuthViewSet

router = DefaultRouter()
router.register(r"titles", TitleViewSet)
router.register(r"genres", GenreViewSet)
router.register(r"categories", CategoryViewSet)
router.register(r"users", UserViewSet),
router.register(r"titles/(?P<title_id>[\d]+)/reviews", ReviewViewSet)
router.register(r"titles/(?P<title_id>[\d]+)/reviews/(?P<review_id>[\d]+)/comments", CommentViewSet)
urlpatterns = router.urls

urlpatterns += [
    path('auth/email/', AuthViewSet.as_view()),
    path('auth/token/', TokenViewSet.as_view(), name='token_obtain'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
