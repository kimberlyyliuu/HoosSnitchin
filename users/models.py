from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    is_site_admin = models.BooleanField(default=False)
    created_message_boards = models.OneToOneField(
        "message_boards.MessageBoard", on_delete=models.CASCADE, null=True, blank=True
    )
    created_comments = models.OneToOneField(
        "message_boards.Comment", on_delete=models.CASCADE, null=True, blank=True
    )

    def __str__(self):
        return self.username
