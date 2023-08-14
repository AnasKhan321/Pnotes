from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
User = get_user_model()


class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    Note_title = models.CharField(max_length=100, blank=True)
    Note_Description = models.TextField(blank=True)

    def __str__(self):
        return self.user.username