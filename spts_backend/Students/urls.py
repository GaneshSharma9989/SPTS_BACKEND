from django.urls import path
from .views import  student_crud, student_list  

urlpatterns = [      
    path('students/', student_crud),          # CRUD
    path('students/list/', student_list),     # Pagination + filter
]