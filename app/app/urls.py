from django.contrib import admin
from django.urls import path, include
from rest_framework_nested import routers
from core import views

router = routers.DefaultRouter()
router.register('schools', views.SchoolViewSet)
router.register('students', views.StudentViewSet)

student_router = routers.NestedSimpleRouter(router, 'schools', lookup='schools')
student_router.register('students', views.StudentViewSet, basename='schools-students')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('', include(student_router.urls)),
]
