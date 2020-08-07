from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.CharField(max_length=1000)
    date = models.DateField()
    time = models.TimeField()

    def __str__(self):
        return f"{self.user} said {self.post} on {self.date} at {self.time}"


class Follow(models.Model):
    follow = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")
    followee = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followers")

    def __str__(self):
        return f"{self.follow} followed {self.followee} and {self.followee} followed by {self.follow}"

    def is_valid_follow(self):
        return self.follow != self.followee


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")
    like = models.IntegerField()

    def __str__(self):
        return f"{self.user} liked {self.post}"

    def is_valid_like(self):
        return self.like == 1