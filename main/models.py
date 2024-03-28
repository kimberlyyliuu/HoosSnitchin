from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    is_site_admin = models.BooleanField(default=False)

    def __str__(self):
        return self.username


class Event(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.title


class Document(models.Model):
    document = models.FileField()
    created_at = models.DateTimeField(default=timezone.now)
    title = models.CharField(max_length=100, default="No title")

    def __str__(self):
        return self.title


class Report(models.Model):
    description = models.TextField()
    date_time = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, null=True, blank=True
    )
    event = models.ForeignKey("Event", on_delete=models.CASCADE)
    document = models.ManyToManyField("Document", blank=True)
    is_in_review = models.BooleanField(default=False)
    is_resolved = models.BooleanField(default=False)
    admin_notes = models.TextField()

    def __str__(self):
        return self.description
