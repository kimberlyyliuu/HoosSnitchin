from django.contrib import admin
from main.models import CustomUser, MessageBoard, Comment, Document

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(MessageBoard)
admin.site.register(Comment)
admin.site.register(Document)
