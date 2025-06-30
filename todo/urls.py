from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    
    path("", views.todo_list, name="todo_list"),
    path("task/create/", views.task_create, name="task_create"),
    path("task/<int:pk>/", views.task_detail, name="task_detail"),
    path("task/<int:pk>/delete/", views.task_delete, name="task_delete"),
    path("task/<int:pk>/complete/", views.task_make_completed, name="task_complete"),
    
    path("register/", views.register, name="register"),
    path("login/", auth_views.LoginView.as_view(template_name='todo/login.html'), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
]
