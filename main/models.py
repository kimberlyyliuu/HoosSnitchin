from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    is_site_admin = models.BooleanField(default=False)

    def __str__(self):
        return self.username

class School(models.Model):
    name = models.CharField(max_length=200)
    #Can add additional fields

    def __str__(self):
        return self.name

class MessageBoard(models.Model):
    admin = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="created_message_boards"
    )
    school = models.ForeignKey(
        School, on_delete=models.CASCADE, related_name="message_boards"
    )
    title = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.title


class Comment(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="user_comments"
    )
    message_board = models.ForeignKey(
        MessageBoard, on_delete=models.CASCADE, related_name="comments"
    )
    comment_text = models.TextField()

    def __str__(self):
        return f"{self.user.username}: {self.comment_text[:50]}"
