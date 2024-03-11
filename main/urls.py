from django.urls import path

from . import views

app_name = "main"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path('logout/', views.LogoutView, name='logout'),
    path('select_school/', views.select_school, name='select_school'),
]
