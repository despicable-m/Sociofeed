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
        f"{self.user} said {self.post} on {self.date} at {self.time}"
