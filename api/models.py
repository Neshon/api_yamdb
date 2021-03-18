from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=False)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=False)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.TextField(max_length=200)
    year = models.IntegerField()
    category = models.ForeignKey(Category,
                                 on_delete=models.SET_NULL,
                                 related_name="title",
                                 blank=True,
                                 null=True)
    genre_title = models.ManyToManyField(Genre)

    def __str__(self):
        return self.name


class Review(models.Model):
    title_id = models.ForeignKey(Title, on_delete=models.CASCADE, related_name="review", name="title")
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="review")
    score = models.IntegerField()
    pub_date = models.DateTimeField("Дата добавления", auto_now_add=True, db_index=True)


class Comment(models.Model):
    review_id = models.ForeignKey(Review, on_delete=models.CASCADE, related_name="comments", name="review")
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    pub_date = models.DateTimeField("Дата добавления", auto_now_add=True, db_index=True)
