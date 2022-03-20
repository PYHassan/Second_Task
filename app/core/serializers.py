from rest_framework.serializers import ModelSerializer
from .models import School, Student


class SchoolSerializer(ModelSerializer):
    class Meta:
        model = School
        fields = '__all__'


class StudentSerializer(ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'
