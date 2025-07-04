from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
import json
from .models import Student, Assessment, Score
@csrf_exempt
def assessments_list_create(request):
    if request.method == "GET":
        assessments = Assessment.objects.all().values('id', 'title', 'chapter', 'week', 'total_marks')
        return JsonResponse(list(assessments), safe=False)

    elif request.method == "POST":
        try:
            data = json.loads(request.body)
            assessment = Assessment.objects.create(
                title=data.get("title"),
                chapter=data.get("chapter"),
                week=data.get("week"),
                total_marks=data.get("total_marks")
            )
            return JsonResponse({"message": "Assessment created", "id": assessment.id}, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)


@csrf_exempt
def assessment_detail(request, id):
    try:
        assessment = Assessment.objects.get(id=id)
    except Assessment.DoesNotExist:
        return JsonResponse({"error": "Assessment not found"}, status=404)

    if request.method == "PUT":
        try:
            data = json.loads(request.body)
            assessment.title = data.get("title")
            assessment.chapter = data.get("chapter")
            assessment.week = data.get("week")
            assessment.total_marks = data.get("total_marks")
            assessment.save()
            return JsonResponse({"message": "Assessment updated"}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    elif request.method == "DELETE":
        assessment.delete()
        return JsonResponse({"message": "Assessment deleted"}, status=200)

    return JsonResponse({"message": "Method not allowed"}, status=405)


@csrf_exempt
def score_list(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

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

        return JsonResponse(list(scores), safe=False)


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


