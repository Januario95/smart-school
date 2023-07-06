from django.urls import path

from .views_admin import (
    profile_view,
    
	home, ver_list_de_professores,
	lista_de_estudantes,

	student_details, student_personal_details,
    student_list_details, notas_de_estudantes, 
    presenca_de_estudantes, register_student,
    
	all_students,
	student_school_details, student_parents_details,
	student_academic_performance, student_statistics,
    student_self_registration, 

	register_teacher, admin_regiser_student_subject, teacher_timetables,
    teacher_add_subject, register_teacher_subject,
    teacher_attedances_page, teacher_take_attendance,
    teacher_check_attendance,
	teacher_details, teacher_personal_details,
	teacher_school_details, teacher_list_details,
    teacher_subject_details,

	register_page,
	login_page,
	logout_page,

	# APIs
	get_all_students_in_a_year,
	get_teacher_semester_info,
    
	teacher_subject_info_api,
    capture_teacher_attendance_api,

	get_semester_marks_api,
	get_semester_attendance_api,
	get_attendance,
	get_semester,
	get_subject_tests_api,
	student_details_api,
	teacher_details_api,
	get_student_pass_fail_stats,
)

app_name = 'app2'

urlpatterns = [
	# APIs
	path('teacher_subject_info_api/<int:semesterPk>/<int:teacherPk>/<str:semesterYear>/<str:semesterName>/<str:semesterClasse>/<str:semesterTurma>/', teacher_subject_info_api),
	path('capture_teacher_attendance_api/<int:teacher_pk>/<str:class_date>/<str:class_time>/<str:attended>/<str:classe_name>/<str:turma_name>/<str:subject_name>/', capture_teacher_attendance_api),

	path('get_all_students_in_a_year/<str:year_name>/', get_all_students_in_a_year),
	path('get_teacher_semester_info/<str:semester_name>/<str:year>/<str:classe>/<str:turma>/', get_teacher_semester_info),

	path('get_semester_marks_api/<str:semester_name>/<int:student_pk>/<str:year>/<str:classe>/<str:turma>/', get_semester_marks_api),
	path('get_semester_attendance_api/<str:semester_name>/<int:student_pk>/<str:year>/<str:classe>/<str:turma>/', get_semester_attendance_api),
	path('get_attendance/<int:semester_pk>/<int:teacher_pk>/<int:student_pk>/<int:subject_pk>/<str:semester_year>/<str:semester_classe>/<str:semester_turma>/',
      	get_attendance),
	path('semester/<int:pk>/', get_semester),
	path('get_subject_tests_api/<int:pk>/<str:subject_name>/',
		 get_subject_tests_api),
	path('student_details_api/<int:pk>/',
		 student_details_api),
	path('teacher_details_api/<int:pk>/',
		 teacher_details_api),
	path('student_pass_fail_stats/<str:semester>/<str:classe>/<str:turma>/',
		 get_student_pass_fail_stats),
         
	path('', home, name='home'),

	path('registar/', register_page, name='register'),
	path('entrar/', login_page, name='login'),
    path('perfil/',profile_view, name='profile'),
	path('sair/', logout_page, name='logout'),

	path('registar-professor/', register_teacher, name='register_teacher'),
    path('admin-registar-estudante/', admin_regiser_student_subject, name='admin_regiser_student_subject'),
	
	path('professores/', ver_list_de_professores,
		 name='ver_list_de_professores'),
    path('professores-detalhes/', teacher_list_details,
         name='teacher_list_details'),
	path('detalhes-do-professor/<int:pk>/',
		 teacher_details, name='teacher_details'),
	path('professores-detalhes-dados-pessoais/<int:pk>/',
		 teacher_personal_details,
		 name='teacher_personal_details'),
	path('professores-detalhes-dados-escolares/<int:pk>/',
		 teacher_school_details,
		 name='teacher_school_details'),
    path('professores-detalhes-disciplinas/<int:pk>/', teacher_subject_details,
          name='teacher_subject_details'),
    path('professores-detalhes-horarios/', teacher_timetables, name='teacher_timetables'),
    path('professores-presencas/', teacher_attedances_page, name='teacher_attedances_page'),
    path('professores-actualizar-presenca/', teacher_take_attendance, name='teacher_take_attendance'),
    path('professores-ver-presenca/', teacher_check_attendance, name='teacher_check_attendance'),
    path('professores-adicionar-disciplina/<int:pk>/', teacher_add_subject, name='teacher_add_subject'),
	# path('professores-actualizar-disciplinas/<int:pk', register_teacher_subject, name='register_teacher_subject'),

	path('estudantes-todos/', all_students, name='all_students'),
	path('estudantes/', lista_de_estudantes,
		 name='lista_de_estudantes'),
    path('estudantes-detalhes/', student_list_details,
         name='detalhes_do_estudante'),
    path('estudantes-notas/', notas_de_estudantes,
          name='notas_de_estudantes'),
    path('estudantes-registar/', register_student, name='register_student'),
    path('estudantes-presenca/', presenca_de_estudantes,
         name='presenca_de_estudantes'),
    path('estudantes-detalhes/<int:pk>/',
		 student_details, name='student_details'),
	path('estudantes-detalhes-dados-pessoais/<int:pk>/',
		 student_personal_details, 
		 name='student_personal_details'),
    path('estudantes-detalhes-dados-escolares/<int:pk>/',
		 student_school_details,
		 name='student_school_details'),
    path('estudantes-detalhes-encarregado-de-educacao/<int:pk>/',
		 student_parents_details,
		 name='student_parents_details'),
	path('estudantes-detalhes-desempenho-academico/<int:pk>/',
		 student_academic_performance, name='student_academic_performance'),
	path('estudantes-detalhes-estatistica/', student_statistics,
		 name='student_statistics'),
         
	path('criar-conta-de-estudante/', student_self_registration, name='student_self_registration'),
]