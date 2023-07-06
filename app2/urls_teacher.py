from django.urls import path, include

from .views_teacher import (
    teacher_homepage, teacher_presencas, teacher_view_attendance,
    teacher_take_presencas,
    teacher_take_presencas_by_list, teacher_take_presencas_by_qrcode,
    teacher_students_info,
    
    teacher_marks, teacher_marks_view, teacher_marks_all_view,
    teacher_marks_add_manually, teacher_marks_add_from_file, teacher_add_marks_api,
    
    teacher_timetable, teacher_profile, teacher_profile_personal_info,
    teacher_profile_update_acc_info, teacher_profile_school_info,
    teacher_profile_student_info,

    attandance_form, attandance_qrcode, teacher_record_attendance,
)

app_name = 'teacher_app'


urlpatterns = [
    path('professor/<int:teacher_pk>/', teacher_homepage, name='teacher_homepage'),
    
    path('professor-presencas/<int:teacher_pk>/', teacher_presencas,  name='teacher_presencas'),
    path('professor-ver-presencas/<int:teacher_pk>/', teacher_view_attendance, name='teacher_view_attendance'),
    path('professor-marcar-presencas/<int:teacher_pk>/', teacher_take_presencas, name='teacher_take_presencas'),
    path('professor-marcar-presencas-lista/<int:teacher_pk>/', teacher_take_presencas_by_list,
         name='teacher_take_presencas_by_list'),
    path('professor-marcar-presencas-qrcode/<int:teacher_pk>/', teacher_take_presencas_by_qrcode,
         name='teacher_take_presencas_by_qrcode'),
 
    path('professor-estudantes/<int:teacher_pk>/', teacher_students_info, name='teacher_students_info'),

    path('professor-marcar-prensenca-api/<int:teacher_pk>/<int:student_pk>/<str:year>/<str:semester>/<str:classe>/<str:turma>/<str:subject>/<str:attended>/', teacher_record_attendance),
    path('professor-presenca-form/<int:teacher_pk>/<int:student_pk>/<str:year>/<str:semester>/<str:classe>/<str:turma>/<str:subject>/', attandance_form, name='attandance_form'),
    path('qrcode/<int:teacher_pk>/<int:student_pk>/<str:year>/<str:semester>/<str:classe>/<str:turma>/<str:subject>/', attandance_qrcode, name='attandance_qrcode'),

    path('professor-notas/<int:teacher_pk>/', teacher_marks, name='teacher_marks'),
    path('professor-notas-ver-por-disciplina/<int:teacher_pk>/', teacher_marks_view, name='teacher_marks_view'),
    path('professor-notas-ver-todas-disciplinas/<int:teacher_pk>/', teacher_marks_all_view, name='teacher_marks_all_view'),
    path('professor-notas-adicionar-por-estudante/<int:teacher_pk>/', teacher_marks_add_manually,
         name='teacher_marks_add_manually'),
    path('professor-notas-adicionar-do-ficheiro/<int:teacher_pk>/', teacher_marks_add_from_file,
         name='teacher_marks_add_from_file'),
    path('teacher_add_marks_api/', teacher_add_marks_api),

    path('professor-horario/<int:teacher_pk>/', teacher_timetable, name='teacher_timetable'),

    path('professor-perfil/<int:teacher_pk>/', teacher_profile, name='teacher_profile'),
    path('professor-perfil-dados-pessoais/<int:teacher_pk>/', teacher_profile_personal_info,
         name='teacher_profile_personal_info'),
    path('professor-perfil-actualizar-conta/<int:teacher_pk>/', teacher_profile_update_acc_info,
         name='teacher_profile_update_acc_info'),
    path('professor-perfil-dados-escolares/<int:teacher_pk>/', teacher_profile_school_info,
         name='teacher_profile_school_info'),
    path('teacher_profile_student_info/<int:teacher_pk>/<int:student_pk>/<str:year_name>/<str:semester_name>/<str:classe_name>/<str:turma_name>/', teacher_profile_student_info),
]