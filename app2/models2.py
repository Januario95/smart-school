from django.db import models

class SemesterNewModel(models.Model):
    SEMESTERS = ((semester, semester) for semester in ('Primeiro', 'Segundo', 'Terceiro'))
    name = models.CharField(
        max_length=20, choices=SEMESTERS
    )
    year = models.CharField(max_length=4)

    def __init__(self):
        return self.name
    
class ClasseNewModel(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name
    
class TurmaNewModel(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name
    
class TestNewModel(models.Model):
    name = models.CharField(max_length=150)
    mark = models.DecimalField(decimal_places=2, max_digits=10)

    def __str__(self):
        return f'{self.name} {self.mark}'

class SubjectNameNewModel(models.Model):
    name = models.CharField(max_length=150)
    turma = models.ForeignKey(
        to=TurmaNewModel, on_delete=models.CASCADE)
    classe = models.ForeignKey(
        to=ClasseNewModel, on_delete=models.CASCADE)
    semester = models.ForeignKey(
        to=SemesterNewModel, on_delete=models.CASCADE)
    tests = models.ManyToManyField(to=TestNewModel)

    def __str__(self):
        return self.name