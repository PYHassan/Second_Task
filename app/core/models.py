from django.db import models
# Create your models here.
from rest_framework.exceptions import PermissionDenied
from rest_framework import status
from uuid import uuid4
from django.db import IntegrityError

#check status of the school
class SchoolIsFull(PermissionDenied):
    status_code = status.HTTP_400_BAD_REQUEST
    default_code = 'invalid'

    def __init__(self, num, status_code=None):
        self.detail = f'The school is already full. , Max students = {num}'
        if status_code is not None:
            self.status_code = status_code


class School(models.Model):
    school_name = models.CharField(max_length=20, unique=True)
    max_students = models.IntegerField()

    def __str__(self):
        return self.school_name


class Student(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    age = models.PositiveSmallIntegerField(blank=True, null=True)
    nationality = models.CharField(max_length=20, blank=True)
    student_id = models.CharField(max_length=20, unique=True, editable=False)
    student_school = models.ForeignKey(School, db_column='school_id', on_delete=models.CASCADE)

    def __str__(self):
        return self.first_name

    def save(self, *args, **kwargs):
        # Validate school's capacity
        student_school = School.objects.filter(school_name=self.student_school)[0]
        max_students_allowed = student_school.max_students
        students_set = student_school.student_set
        # If the student exist then update the student
        if not students_set.filter(id=self.id).exists():
            current_students = len(students_set.all())
            #If the school is full of students
            if current_students >= max_students_allowed:
                raise SchoolIsFull(student_school.max_students)
        self.student_id = uuid4().hex[: 20]
        super(Student, self).save(*args, **kwargs)
