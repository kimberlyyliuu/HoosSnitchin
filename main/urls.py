from django.urls import path

from . import views

app_name = "main"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("admin_view/<str:post_type>/", views.admin_view, name="admin_view"),
    path(
        "bring_report_to_review/",
        views.bring_report_to_review,
        name="bring_report_to_review",
    ),
    path("report/event<int:event_id>/", views.report_upload_view, name="report_upload"),
    path(
        "report/<int:report_id>/upload/",
        views.document_upload_view,
        name="document_upload",
    ),
    path("my_reports/", views.my_reports, name="my_reports"),
    path("delete_report/<int:report_id>/", views.delete_report, name="delete_report"),
    path(
        "delete_report_admin/<int:report_id>/",
        views.delete_report_admin,
        name="delete_report_admin",
    ),
    # override default logout view (logs out and redirects to index)
    path("accounts/logout/", views.logout_view, name="custom-logout"),
]
