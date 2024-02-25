from django.db import models


class MessageBoard(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.title


class Comment(models.Model):
    message_board = models.ForeignKey(
        MessageBoard, on_delete=models.CASCADE, related_name="comments"
    )
    comment = models.TextField()

    def __str__(self):
        return self.comment
