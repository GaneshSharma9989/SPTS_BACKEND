from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Assessment
from .models import Student, Assessment, Score
import json
from users.views import TOKENS

def authenticate_request(request):
    token = request.headers.get("Authorization")
    return token in TOKENS

@csrf_exempt
def assessment_data(request):
    if request.method == "GET":
        assessments = Assessment.objects.all().values('id', 'title', 'chapter', 'week', 'total_marks')
        return JsonResponse(list(assessments), safe=False)
    return JsonResponse({"message": "Only GET method allowed"}, status=405)

@csrf_exempt
def score_list(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            print("Received data:", data)

            student_id = data.get("student_id")
            assessment_id = data.get("assessment_id")
            marks = data.get("marks")
            student_obj = Student.objects.get(id=student_id)
            assessment_obj = Assessment.objects.get(id=assessment_id)

            Score.objects.create(
                student=student_obj,
                assessment=assessment_obj,
                marks=marks
            )

            return JsonResponse({"message": "Score added successfully."}, status=201)

        except Exception as e:
            print("Error:", e)
            return JsonResponse({"error": str(e)}, status=500)

    elif request.method == "GET":
        scores = list(Score.objects.values())
        return JsonResponse(scores, safe=False)
    

@csrf_exempt
def progress_by_student(request, student_id):
    if request.method == "GET":
        scores = Score.objects.filter(student_id=student_id).values(
            "assessment__week",
            "assessment__title",
            "assessment__total_marks",
            "marks"
        )

        if not scores:
            return JsonResponse({"error": "No scores found for this student"}, status=404)

        progress = list(scores)
        return JsonResponse(progress, safe=False)
    

@csrf_exempt
def report_by_student(request, student_id):
    if request.method == "GET":
        scores = Score.objects.filter(student_id=student_id).select_related('assessment', 'student')
        
        if not scores.exists():
            return JsonResponse({"error": "No scores found for this student"}, status=404)

        student = scores[0].student

        report_data = []
        total_obtained = 0
        total_possible = 0

        for score in scores:
            marks = score.marks
            total = score.assessment.total_marks
            total_obtained += marks
            total_possible += total

            report_data.append({
                "id": score.assessment.id,  
                "assessment": score.assessment.title,
                "chapter": score.assessment.chapter,
                "week": score.assessment.week,
                "marks_obtained": marks,
                "total_marks": total,
                "percentage": round((marks / total) * 100, 2) if total > 0 else 0
            })

        overall_percentage = round((total_obtained / total_possible) * 100, 2) if total_possible > 0 else 0

        return JsonResponse({
            "student": student.name,
            "report": report_data,
            "total_marks_obtained": total_obtained,
            "total_marks_possible": total_possible,
            "overall_percentage": overall_percentage
        }, safe=False)
