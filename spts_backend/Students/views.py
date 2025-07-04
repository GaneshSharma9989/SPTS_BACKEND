from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from Students.models import Student
from django.core.paginator import Paginator
from django.db.models import Q
import json

@csrf_exempt
def student_crud(request):
    try:
        if request.method == "GET":
            student_id = request.GET.get("id")
            if student_id:
                try:
                    student = Student.objects.get(id=student_id)
                    return JsonResponse({
                        "id": student.id,
                        "name": student.name,
                        "class_name": student.class_name,
                        "section": student.section
                    }, status=200)
                except Student.DoesNotExist:
                    return JsonResponse({"error": "Student not found"}, status=404)
            else:
                students = Student.objects.all().values('id', 'name', 'class_name', 'section')
                return JsonResponse(list(students), safe=False)

        elif request.method == "POST":
            data = json.loads(request.body)
            student = Student.objects.create(
                name=data["name"],
                class_name=data["class_name"],
                section=data["section"]
            )
            return JsonResponse({"message": "Student created", "id": student.id}, status=201)

        elif request.method == "PUT":
            data = json.loads(request.body)
            student_id = data.get("id")
            if not student_id:
                return JsonResponse({"error": "ID required for update"}, status=400)

            try:
                student = Student.objects.get(id=student_id)
                student.name = data.get("name", student.name)
                student.class_name = data.get("class_name", student.class_name)
                student.section = data.get("section", student.section)
                student.save()
                return JsonResponse({"message": "Student updated"}, status=200)
            except Student.DoesNotExist:
                return JsonResponse({"error": "Student not found"}, status=404)

        elif request.method == "DELETE":
            data = json.loads(request.body)
            student_id = data.get("id")
            if not student_id:
                return JsonResponse({"error": "ID required for deletion"}, status=400)

            try:
                student = Student.objects.get(id=student_id)
                student.delete()
                return JsonResponse({"message": "Student deleted"}, status=200)
            except Student.DoesNotExist:
                return JsonResponse({"error": "Student not found"}, status=404)

        return JsonResponse({"error": "Invalid method"}, status=405)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
def student_list(request):
    if request.method == "GET":
        class_name = request.GET.get("class", "").strip()
        section = request.GET.get("section", "").strip()
        page = int(request.GET.get("page", 1))
        per_page = 2  # 2 students per page

        students = Student.objects.all()

        if class_name:
            students = students.filter(class_name__iexact=class_name)
        if section:
            students = students.filter(section__iexact=section)

        paginator = Paginator(students, per_page)
        page_obj = paginator.get_page(page)

        student_data = list(page_obj.object_list.values('id', 'name', 'class_name', 'section'))

        response_data = {
            "total": paginator.count,
            "pages": paginator.num_pages,
            "current": page_obj.number,
            "students": student_data
        }

        return JsonResponse(response_data)

    elif request.method == "POST":
        data = json.loads(request.body)
        student = Student.objects.create(**data)
        return JsonResponse({"message": "Student created", "id": student.id})