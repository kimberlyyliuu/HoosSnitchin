from django.urls import path
from main.views import document_upload_view

from . import views

app_name = "main"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("logout/", views.LogoutView, name="logout"),
    path("upload/", document_upload_view, name="document_upload"),
    path("admin-view/", views.admin_view, name="admin-view"),
]
