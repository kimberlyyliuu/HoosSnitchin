from django.urls import path

from . import views

app_name = "main"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path('logout/', views.LogoutView, name='logout'),
    path('pickschool/', views.school_list, name='school_list'),
]
