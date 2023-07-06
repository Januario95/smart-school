from django.urls import path

from .views_student import (
    student_profile, student_update_profile, student_teachers,
    student_profile_teacher_info, student_profile_teacher_info,
    student_view_attendance, student_view_attendance_by_subject,
)

app_name = 'student_app'

urlpatterns = [
    path('estudante-perfil/<int:student_pk>/', student_profile, name='student_profile'),
    path('estudente-perfil-actualizar/<int:student_pk>/', student_update_profile,
         name='student_update_profile'),
    path('estudante-professores/<int:student_pk>/', student_teachers, name='student_teachers'),
    path('estudante-presenca/<int:student_pk>/', student_view_attendance, name='student_view_attendance'),
    path('estudane-presenca-por-disciplina/<int:student_pk>/', student_view_attendance_by_subject,
         name='student_view_attendance_by_subject'),

    path('student_profile_teacher_info/<int:teacher_pk>/<int:student_pk>/<str:year_name>/<str:semester_name>/<str:classe_name>/<str:turma_name>/', student_profile_teacher_info),
]

