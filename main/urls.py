from django.urls import path

from . import views

app_name = "main"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("admin_view/", views.admin_view, name="admin_view"),
    path("update_report/", views.update_report, name="update_report"),
    path("report/event<int:event_id>/", views.report_upload_view, name="report_upload"),
    path(
        "report/<int:report_id>/upload/",
        views.document_upload_view,
        name="document_upload",
    ),
    path("my_reports/", views.my_reports, name="my_reports"),
    path("delete_report/<int:report_id>/", views.delete_report, name="delete_report"),
]
