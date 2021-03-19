from django.urls import path
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView)

from .views import GenreViewSet, CommentViewSet, CategoryViewSet, TitleViewSet

router = DefaultRouter()
router.register(r"titles", TitleViewSet)
router.register(r"genres", GenreViewSet)
router.register(r"categories", CategoryViewSet)
# router.register(r"titles/(?P<id>[0-9]+)/reviews/(?P<id>[0-9]+)/comments", CommentViewSet)
urlpatterns = router.urls

# urlpatterns += [
#     path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
#     path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
#     path('api-token-auth/', views.obtain_auth_token),
# ]