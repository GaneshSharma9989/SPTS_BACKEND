from django.db import models
from Students.models import Student

class Assessment(models.Model):
    title = models.CharField(max_length=100)
    chapter = models.CharField(max_length=100)
    week = models.IntegerField()
    total_marks = models.IntegerField()

    def __str__(self):
        return f"{self.title} - {self.chapter} (Week {self.week})"

class Score(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE)
    marks = models.IntegerField()

    def __str__(self):
        return f"{self.student.name} - {self.assessment.title} - {self.marks_obtained} marks"



