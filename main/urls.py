from django.urls import path

from . import views

app_name = "main"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("logout/", views.LogoutView, name="logout"),
    path("admin-view/", views.admin_view, name="admin-view"),
    path("report/", views.report_upload_view, name="report_upload"),
    path("home_events/", views.eventView, name="home_events"),
    path(
        "report/<int:report_id>/upload",
        views.document_upload_view,
        name="document_upload",
    ),
    path("document_upload/", views.document_upload, name="document_upload"),
    path('my-reports/', views.user_reports, name='mysnitches'),
    path('admin-notes/', views.admin_notes, name='admin-notes'),
    path('update_report/', views.update_report, name='update_report'),
    path('delete_report/<int:report_id>/', views.delete_report, name='delete_report'),
]
