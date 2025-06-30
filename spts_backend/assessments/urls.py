from django.urls import path
from .views import assessment_data, score_list
from .views import progress_by_student
from .views import report_by_student

urlpatterns = [
    path('assessments/', assessment_data),
    path('scores/', score_list),
    path('progress/<int:student_id>/', progress_by_student), 
    path('report/<int:student_id>/', report_by_student),
]