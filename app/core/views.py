from .models import School, Student
from .serializers import SchoolSerializer, StudentSerializer
from rest_framework import viewsets, filters
from django.shortcuts import get_object_or_404


class SchoolViewSet(viewsets.ModelViewSet):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer
    filter_backends = [filters.SearchFilter]
    # SearchFilter for search for specific student
    search_fields = ['school_name']


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['first_name', 'last_name']

    def get_queryset(self):
        if self.kwargs.get('school_pk'):
            return Student.objects.filter(school=self.kwargs.get('school_pk'))
        else:
            return Student.objects.all()

    def create(self, request, school_pk=None,  *args, **kwargs):
        if not school_pk:
            return super(StudentViewSet, self).create(request, *args, **kwargs)
        school = get_object_or_404(School.objects.filter(pk=school_pk))
        _mutable = None
        if hasattr(request.data, '_mutable'):
            _mutable = request.data._mutable
            request.data._mutable = True
            request.data['school'] = school.pk
            request.data._mutable = _mutable
        else:
            request.data['school'] = school.pk
        return super(StudentViewSet, self).create(request, *args, **kwargs)

    def update(self, request, school_pk=None,  *args, **kwargs):
        if not school_pk:
            return super(StudentViewSet, self).update(request, *args, **kwargs)
        school = get_object_or_404(School.objects.filter(pk=school_pk))
        _mutable = None
        if hasattr(request.data, '_mutable'):
            _mutable = request.data._mutable
            request.data._mutable = True
            request.data['school'] = school.pk
            request.data._mutable = _mutable
        else:
            request.data['school'] = school.pk
        return super(StudentViewSet, self).update(request, *args, **kwargs)
