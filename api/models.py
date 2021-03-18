from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


User = get_user_model()


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
                                 related_name="category",
                                 blank=True,
                                 null=True)
    # description = models.TextField(null=True, blank=True)
    genre = models.ManyToManyField(Genre, "genre")

    def __str__(self):
        return self.name


class Review(models.Model):
    title = models.ForeignKey(Title, on_delete=models.CASCADE, related_name="title")
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="author")
    score = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    pub_date = models.DateTimeField(auto_now_add=True, db_index=True)


class Comment(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name="review")
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    pub_date = models.DateTimeField(auto_now_add=True, db_index=True)
