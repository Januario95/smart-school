from rest_framework.viewsets import ModelViewSet

from app2.models import (
    SemesterNewModel, ClasseNewModel, TurmaNewModel,
    TestNewModel, StudentNameNewModel, SubjectNewModel,
    SubjectNameNewModel
)
from app2.serializers import (
    SemesterNewModelSerializer, ClasseNewModelSerializer, TurmaNewModelSerializer,
    TestNewModelSerializer, StudentNameNewModelSerializer, SubjectNewModelSerializer,
    SubjectNameNewModelSerializer
)

class SemesterNewModelView(ModelViewSet):
    queryset = SemesterNewModel.objects.all()
    serializer_class = SemesterNewModelSerializer

class ClasseNewModelView(ModelViewSet):
    queryset = ClasseNewModel.objects.all()
    serializer_class = ClasseNewModelSerializer

class TurmaNewModelView(ModelViewSet):
    queryset = TurmaNewModel.objects.all()
    serializer_class = TurmaNewModelSerializer

class TestNewModelView(ModelViewSet):
    queryset = TestNewModel.objects.all()
    serializer_class = TestNewModelSerializer

class StudentNameNewModelView(ModelViewSet):
    queryset = StudentNameNewModel.objects.all()
    serializer_class = StudentNameNewModelSerializer

class SubjectNewModelView(ModelViewSet):
    queryset = SubjectNewModel.objects.all()
    serializer_class = SubjectNewModelSerializer

class SubjectNameNewModelView(ModelViewSet):
    queryset = SubjectNameNewModel.objects.all()
    serializer_class = SubjectNameNewModelSerializer