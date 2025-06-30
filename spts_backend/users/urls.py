from django.urls import path
from . import views

urlpatterns = [
     path('register/', views.register_teacher, name='register'),
    path('login/', views.login_teacher, name='login'),
    path('reset-password/', views.reset_password),
    path('users/', views.get_users)
]
