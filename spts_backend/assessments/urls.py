from django.urls import path
from .views import (
    assessments_list_create,
    assessment_detail,
    score_list,
    progress_by_student,
    report_by_student
)

urlpatterns = [
    path('assessments/', assessments_list_create),           
    path('assessments/<int:id>/', assessment_detail),        
    path('scores/', score_list),                             
    path('progress/<int:student_id>/', progress_by_student),
    path('report/<int:student_id>/', report_by_student),
]

