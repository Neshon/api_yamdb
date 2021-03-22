from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class User(AbstractUser):
    class UserRoles:
        USER = 'user'
        MODERATOR = 'moderator'
        ADMIN = 'admin'

        choices = [
            (USER, USER),
            (MODERATOR, MODERATOR),
            (ADMIN, ADMIN),
        ]

    role = models.CharField(max_length=9, choices=UserRoles.choices, default=UserRoles.USER)
    bio = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(unique=True)
    confirmation_code = models.CharField(max_length=9, blank=True)

    @property
    def is_admin(self):
        return self.role == self.UserRoles.ADMIN or self.is_staff

    @property
    def is_moderator(self):
        return self.role == self.UserRoles.MODERATOR


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.TextField(max_length=200)
    year = models.IntegerField()
    category = models.ForeignKey(Category,
                                 on_delete=models.SET_NULL,
                                 related_name="titles",
                                 blank=True,
                                 null=True)
    description = models.TextField(null=True, blank=True)
    genre = models.ManyToManyField(Genre, related_name="titles")

    def __str__(self):
        return self.name


class Review(models.Model):
    title = models.ForeignKey(Title, on_delete=models.CASCADE, related_name="review")
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="review")
    score = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    pub_date = models.DateTimeField(auto_now_add=True, db_index=True)


class Comment(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name="comment")
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment")
    pub_date = models.DateTimeField(auto_now_add=True, db_index=True)
