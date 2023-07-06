from rest_framework import serializers

from app2.models import (
    SemesterNewModel, ClasseNewModel, TurmaNewModel,
    TestNewModel, StudentNameNewModel, SubjectNewModel,
    SubjectNameNewModel
)

class SemesterNewModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = SemesterNewModel
        fields = '__all__'
        depth = 3

class ClasseNewModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClasseNewModel
        fields = '__all__'
        depth = 3

class TurmaNewModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = TurmaNewModel
        fields = '__all__'
        depth = 3

class TestNewModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestNewModel
        fields = '__all__'
        depth = 3


class StudentNameNewModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentNameNewModel
        fields = '__all__'
        depth = 3

class SubjectNewModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubjectNewModel
        fields = '__all__'
        depth = 3

class SubjectNameNewModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubjectNameNewModel
        fields = '__all__'
        depth = 3