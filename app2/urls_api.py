from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .api import (
    SemesterNewModelView, ClasseNewModelView, TurmaNewModelView,
    TestNewModelView, StudentNameNewModelView, StudentNameNewModelView,
    SubjectNewModelView, SubjectNameNewModelView,
)

router = DefaultRouter()
router.register('semesters', SemesterNewModelView)
router.register('classes', ClasseNewModelView)
router.register('turmas', TurmaNewModelView)
router.register('tests', TestNewModelView)
router.register('students', StudentNameNewModelView)
router.register('subjects', SubjectNewModelView)
router.register('subject-names', SubjectNameNewModelView)

urlpatterns = [
    path('', include(router.urls)),
]