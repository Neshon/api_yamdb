from rest_framework import viewsets, filters
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import BasePermission, IsAuthenticated, IsAuthenticatedOrReadOnly

from .models import Title, Comment, Genre, Category, User
from .serializers import CategorySerializer, CommentSerializer, TitleSerializer, GenreSerializer


class OwnResourcePermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in ("DELETE", "PUT", "POST", "PATCH"):
            return request.user == obj.author
        return True


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    # permission_classes = [OwnResourcePermission, IsAuthenticatedOrReadOnly]

    # def get_queryset(self):
    #     queryset = Post.objects.all()
    #     group = self.request.query_params.get('group', None)
    #     if group is not None:
    #         queryset = queryset.filter(group=group)
    #     return queryset
    #
    # def perform_create(self, serializer):
    #     serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    # permission_classes = [OwnResourcePermission, IsAuthenticatedOrReadOnly]

    # def perform_create(self, serializer):
    #     serializer.save(author=self.request.user)


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    # permission_classes = [IsAuthenticatedOrReadOnly]


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # permission_classes = [IsAuthenticatedOrReadOnly]
    # filter_backends = [filters.SearchFilter]
    # search_fields = ['=user__username', '=following__username']
    #
    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)