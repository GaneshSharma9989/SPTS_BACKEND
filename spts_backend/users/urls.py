from django.urls import path
from . import views

urlpatterns = [
     path('register/', views.register_teacher, name='register'),
    path('login/', views.login_teacher, name='login'),
    path('users/', views.get_users)
]
