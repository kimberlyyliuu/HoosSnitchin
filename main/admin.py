from django.contrib import admin
from main.models import CustomUser, MessageBoard, Comment, Event, School, Document

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(MessageBoard)
admin.site.register(Comment)
admin.site.register(Event)
admin.site.register(School)
admin.site.register(Document)
