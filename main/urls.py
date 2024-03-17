from django.urls import path

from . import views

app_name = "main"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("logout/", views.LogoutView, name="logout"),
    path("admin-view/", views.admin_view, name="admin-view"),
    path("report/", views.report_upload_view, name="report_upload"),
    path("home_events/", views.home_events_view, name="home_events"),
    path(
        "report/<int:report_id>/upload",
        views.document_upload_view,
        name="document_upload",
    ),
]
