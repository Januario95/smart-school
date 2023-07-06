from django.urls import path

from .views_admin import (
	home, ver_por_turma, ver_list_de_professores,
	lista_de_estudantes, pesquisar_estudante,
	ver_notas_de_tests,
	student_details, student_personal_details,
	student_school_details, student_parents_details,
	teacher_details, 

	register_page,
	login_page,
	logout_page,

	# APIs
	student_details_api,
	teacher_details_api,
)

app_name = 'app2'

urlpatterns = [
	# APIs
	path('student_details_api/<int:pk>/',
		 student_details_api),
	path('teacher_details_api/<int:pk>/',
		 teacher_details_api),

	path('registar/', register_page, name='register'),
	path('entrar/', login_page, name='login'),
	path('sair/', logout_page, name='logout'),

	path('detalhes-do-estudante/<int:pk>/',
		 student_details, name='student_details'),
	path('detalhes-do-professor/<int:pk>/',
		 teacher_details, name='teacher_details'),
	path('dados-pessoais-do-estudante/<int:pk>/',
		 student_personal_details, 
		 name='student_personal_details'),
	path('dados-escolares-do-estudante/<int:pk>/',
		 student_school_details,
		 name='student_school_details'),
	path('dados-do-encarregado-de-educacao/<int:pk>/',
		 student_parents_details,
		 name='student_parents_details'),

	path('', home, name='home'),
	path('ver-por-turma/', ver_por_turma, name='ver_por_turma'),
	path('professores/', ver_list_de_professores,
		 name='ver_list_de_professores'),
	path('list-de-estudantes/', lista_de_estudantes,
		 name='lista_de_estudantes'),
	path('pesquisar-estudante/', pesquisar_estudante,
		 name='pesquisar_estudante'),
	path('ver-notas-de-tests/', ver_notas_de_tests,
		 name='ver_notas_de_tests'),
]