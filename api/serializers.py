from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Title, Comment, Review, Genre, Category, User


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Genre


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Category


class TitleReadSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.IntegerField(allow_null=True)

    class Meta:
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
        )
        model = Title


class TitleWriteSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(queryset=Category.objects.all(),
                                            slug_field='slug')
    genre = serializers.SlugRelatedField(queryset=Genre.objects.all(),
                                         slug_field='slug', many=True)

    class Meta:
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')
        model = Title


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='username', read_only=True)

    def validate(self, data):
        """Пользователь может оставить только один отзыв на один объект."""
        if self.context['request'].method == 'PATCH':
            return data
        user = self.context['request'].user
        title = self.context['request'].parser_context['kwargs']['title_id']
        if Review.objects.filter(author=user, title_id=title).exists():
            raise serializers.ValidationError('Вы уже поставили оценку')
        return data

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('first_name', 'last_name', 'username', 'bio', 'email', 'role')
        model = User


class AuthSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('email',)
        model = User


class RetrieveTokenSerializer(TokenObtainSerializer):
    email_field = User.EMAIL_FIELD

    def __init__(self, *args, **kwargs):
        super(TokenObtainSerializer, self).__init__(*args, **kwargs)
        self.fields[self.email_field] = serializers.CharField()
        self.fields["confirmation_code"] = serializers.CharField()

    def validate(self, attrs):
        authenticate_kwargs = {
            self.email_field: attrs.get(self.email_field),
            "confirmation_code": attrs.get("confirmation_code"),
        }
        try:
            user = User.objects.get(
                email=authenticate_kwargs[self.email_field],
                confirmation_code=authenticate_kwargs["confirmation_code"],
            )
        except User.DoesNotExist:
            msg = 'Must include.'
            raise serializers.ValidationError(msg)
        if user:
            user.is_active = True
            user.save()
            refresh = RefreshToken.for_user(user)
            return {"token": str(refresh.access_token)}
