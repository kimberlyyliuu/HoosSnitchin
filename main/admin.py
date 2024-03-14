from django.contrib import admin
from main.models import CustomUser, Event, Document, Report

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Event)
admin.site.register(Document)
admin.site.register(Report)
