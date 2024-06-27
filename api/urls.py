from django.urls import path

from .views import Tasks, change_password, loadjson, login, register

app_name = 'api'

urlpatterns = [
    # User
    path('login/', login),
    path('register/', register),
    path('change-password/', change_password),

    # Tasks
    path('tasks/', Tasks.as_view()),
    path('task/<int:id>/', Tasks.as_view()),
    path('task/add/', Tasks.as_view()),

    # Swagger json endpoit
    path('schema-swagger/', loadjson),
]
