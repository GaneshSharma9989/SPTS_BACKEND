from django.db import models
class Student(models.Model):
    name = models.CharField(max_length=100)
    class_name = models.CharField(max_length=20)
    section = models.CharField(max_length=5)
    status = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name}"