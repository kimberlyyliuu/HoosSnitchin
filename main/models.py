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
    title = models.CharField(max_length=255)
    document = models.FileField()
    report = models.ForeignKey(
        "Report", on_delete=models.CASCADE, null=True, blank=True
    )

    def __str__(self):
        return f"{self.title}"


class Report(models.Model):
    description = models.TextField()
    date = models.DateField()
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    event = models.ForeignKey("Event", on_delete=models.CASCADE)

    def __str__(self):
        return self.description
