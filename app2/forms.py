from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from app2.models import (
    SemesterNewModel, ClasseNewModel, TurmaNewModel,
    TestNewModel, StudentNameNewModel, SubjectNewModel,
    SubjectNameNewModel, Year, TeacherNameNewModel
)
from .helpers import (
	COUNTRIES,
)

import os
import string
import random

GENDER = (
	('-----', '-----'),
	('masculino', 'Masculino'),
	('feminino', 'Feminino')
)
PROVINCE = (
	('Cabo Delgado', 'Cabo Delgado'),
	('Gaza', 'Gaza'),
	('Inhabane', 'Inhabane'),
	('Manica', 'Manica'),
	('Maputo', 'Maputo'),
	('Nampula', 'Nampula'),
	('Niassa', 'Niassa'),
	('Sofala', 'Sofala'),
	('Tete', 'Tete'),
	('Zambézia', 'Zambézia')
)
NIVEL_ACADEMICO = (
	('Nível Médio', 'Nivel Medio'),
	('Licenciatura', 'Licenciatura'),
	('Mestrado', 'Mestrado'),
	('Doutoramento', 'Doutoramento'),
)
YEARS = ((x, x) for x in range(2023, 2025))
SEMESTERS = ((semester, semester) for semester in ('Primeiro', 'Segundo', 'Terceiro'))
CLASSES = ((f'{x}ª classe', f'{x}ª classe') for x in range(8, 13))
TURMAS = (
	('A', 'A'),
	('B', 'B'),
	('C', 'C')
)
SUBJECTS = (
	('Matematica', 'Matematica'),
	('Fisica', 'Fisica'),
	('Quimica', 'Quimica'),
	('Biologia', 'Biologia'),
	('Portugues', 'Portugues'),
	('Ingles', 'Ingles')
)
MONTHS = (
	('0', 'Todos'),
    ('1', 'Janeiro'), 
    ('2', 'Fevereiro'), 
    ('3', 'Março'), 
    ('4', 'Abril'), 
    ('5', 'Maio'), 
    ('6', 'Junho'), 
    ('7', 'Julho'), 
    ('8', 'Augusto'), 
    ('9', 'Setembro'), 
    ('10', 'Outubro'), 
    ('11', 'Novembro'), 
    ('12', 'Dezembro')
)

class DateInput(forms.DateInput):
    input_type = 'date'

class MonthInput(forms.DateInput):
    input_type = 'month'
    
def get_n():
    return str(random.randint(0, 9))

def generate_IC():
	nums = [get_n() for _ in range(10)]
	return '02' + ''.join(nums) + random.choice(string.ascii_uppercase)

digits = string.digits
preffix = ['86', '87', '84', '85', '82']

def get_suffix():
	return ''.join([random.choice(digits) for _ in range(7)])

def generate_phone_number():
	return '+258' + random.choice(preffix) + get_suffix()


class RegisterTeacherSubjectForm(forms.Form):
	academic_year = forms.ChoiceField(
		choices=YEARS
	)
	semester = forms.ChoiceField(
		choices=SEMESTERS
	)
	classe = forms.ChoiceField(choices=CLASSES)
	turma = forms.ChoiceField(choices=TURMAS)
	subject = forms.ChoiceField(choices=SUBJECTS)
	# subject = forms.CharField(
	# 	max_length=255,
	# 	widget=forms.TextInput(attrs={
	# 		'value': 'Matematica',
	# 		'placeholder': 'Adicione a disciplina',
	# 		'oninvalid': "this.setCustomValidity('Por favor insira a disciplina aqui')"
	# 	}))



class RegisterStudentForm(forms.Form):
	GENDER = (
		('masculino', 'Masculino'),
		('feminino', 'Feminino')
	)
	YEARS = ((x, x) for x in range(2023, 2025))
	SEMESTERS = ((semester, semester) for semester in ('Primeiro', 'Segundo', 'Terceiro'))
	CLASSES = ((f'{x}ª classe', f'{x}ª classe') for x in range(8, 13))
	TURMAS = (
		('A', 'A'),
		('B', 'B'),
		('C', 'C')
	)
	SUBJECTS = (
		('Matematica', 'Matematica'),
		('Fisica', 'Fisica'),
		('Quimica', 'Quimica'),
		('Biologia', 'Biologia'),
		('Portugues', 'Portugues'),
		('Ingles', 'Ingles')
	)
	username = forms.CharField(
		max_length=255,
		widget=forms.TextInput(attrs={
			'value': 'janedoe',
			'placeholder': 'Insira o nome de usuario',
			'oninvalid': "this.setCustomValidity('Por favor insira nome de usuario aqui')"
		}))
	password = forms.CharField(
		max_length=50,
		widget=forms.PasswordInput(attrs={
			'value': 'Jaci1995',
			'placeholder': 'Escolha a senha',
			'oninvalid': "this.setCustomValidity('Por favor insira a sua senha aqui')"
		}))
	confirm_password = forms.CharField(
		max_length=50,
		widget=forms.PasswordInput(attrs={
			'value': 'Jaci1995',
			'placeholder': 'Confirme a sua senha',
			'oninvalid': "this.setCustomValidity('Por favor confirma a sua senha aqui')"
		}))
	email = forms.CharField(
		widget=forms.EmailInput(attrs={
			'value': 'jane.doe@portal.co.mz',
			'placeholder': 'Insira o seu email aqui',
			'oninvalid': "this.setCustomValidity('Por favor insira o seu email aqui')"
		}))
	first_name = forms.CharField(
		max_length=100,
		widget=forms.TextInput(attrs={
			'value': 'Jane',
			'placeholder': 'Insira o nome de seu primeiro nome',
			'oninvalid': "this.setCustomValidity('Por favor insira o seu nome aqui')"
		}))
	last_name = forms.CharField(
		max_length=100,
		widget=forms.TextInput(attrs={
			'value': 'Doe',
			'placeholder': 'Insira o nome de seu ultimo nome',
			'oninvalid': "this.setCustomValidity('Por favor insira o apelido aqui')"
		}))
	ic_number = forms.CharField(
		max_length=13, 
		widget=forms.TextInput(attrs={
			'value': generate_IC(),
			'placeholder': 'Insira o numero de BI',
			'oninvalid': "this.setCustomValidity('Por favor insira o numero de BI aqui')"
		})
	)
	gender = forms.ChoiceField(choices=GENDER)
	birth_date = forms.DateField(widget=DateInput)
	phone_number = forms.CharField(
	    max_length=13, widget=forms.TextInput(attrs={
		    'value': generate_phone_number(),
			'placeholder': 'Insira o numero de telefone',
			'oninvalid': "this.setCustomValidity('Por favor insira o numero de telefone aqui')"
		}))
	province = forms.ChoiceField(
		choices=PROVINCE)
	city = forms.CharField(
		max_length=50, widget=forms.TextInput(attrs={
			'value': 'Maputo',
			'placeholder': 'Insira a cidade onde moras',
			'oninvalid': "this.setCustomValidity('Por favor insira a cidade onde moras, aqui')"
		}))
	bairro = forms.CharField(
		max_length=50, widget=forms.TextInput(attrs={
			'value': 'Alto Mae',
			'placeholder': 'Insira o seu bairro',
			'oninvalid': "this.setCustomValidity('Por favor insira o seu bairro aqui')"
		}))
	year = forms.ChoiceField(
		choices=YEARS
	)
	semester = forms.ChoiceField(
		choices=SEMESTERS
	)
	classe = forms.ChoiceField(choices=CLASSES)
	turma = forms.ChoiceField(choices=TURMAS)
	# subject = forms.ChoiceField(choices=SUBJECTS)
	subjects = forms.MultipleChoiceField(
        choices = SUBJECTS,
        widget  = forms.CheckboxSelectMultiple,
    )

	# Father information
	father_first_name = forms.CharField(
		max_length=100,
		widget=forms.TextInput(attrs={
			'value': 'Jane',
			'placeholder': 'Insira o nome de seu primeiro nome',
			'oninvalid': "this.setCustomValidity('Por favor insira o seu nome aqui')"
		}))
	father_last_name = forms.CharField(
		max_length=100,
		widget=forms.TextInput(attrs={
			'value': 'Doe',
			'placeholder': 'Insira o nome de seu ultimo nome',
			'oninvalid': "this.setCustomValidity('Por favor insira o apelido aqui')"
		}))
	father_email = forms.CharField(
		max_length=100,
		widget=forms.TextInput(attrs={
			'value': 'john.doe@portal.co.mz',
			'placeholder': 'Insira o email do pai',
			'oninvalid': "this.setCustomValidity('Por favor insira o email do pai aqui')"
		}))
	father_ic_number = forms.CharField(
		max_length=13, 
		widget=forms.TextInput(attrs={
			'value': generate_IC(),
			'placeholder': 'Insira o numero de BI',
			'oninvalid': "this.setCustomValidity('Por favor insira o numero de BI aqui')"
		})
	)
	father_gender = forms.ChoiceField(choices=GENDER)
	father_phone_number = forms.CharField(
	    max_length=13, widget=forms.TextInput(attrs={
		    'value': generate_phone_number(),
			'placeholder': 'Insira o numero de telefone',
			'oninvalid': "this.setCustomValidity('Por favor insira o numero de telefone aqui')"
		}))
	father_profession = forms.CharField(
		max_length=50, widget=forms.TextInput(attrs={
			'value': 'Medico',
			'placeholder': 'Insira a profissao do pai',
			'oninvalid': "this.setCustomValidity('Por favor insira a cprofissao do pai, aqui')"
		}))
	father_province = forms.ChoiceField(
		choices=PROVINCE)
	father_city = forms.CharField(
		max_length=50, widget=forms.TextInput(attrs={
			'value': 'Maputo',
			'placeholder': 'Insira a cidade onde moras',
			'oninvalid': "this.setCustomValidity('Por favor insira a cidade onde moras, aqui')"
		}))
	father_bairro = forms.CharField(
		max_length=50, widget=forms.TextInput(attrs={
			'value': 'Alto Mae',
			'placeholder': 'Insira o seu bairro',
			'oninvalid': "this.setCustomValidity('Por favor insira o seu bairro aqui')"
		}))
	

	# Mother information
	mother_first_name = forms.CharField(
		max_length=100,
		widget=forms.TextInput(attrs={
			'value': 'Jane',
			'placeholder': 'Insira o nome de seu primeiro nome',
			'oninvalid': "this.setCustomValidity('Por favor insira o seu nome aqui')"
		}))
	mother_last_name = forms.CharField(
		max_length=100,
		widget=forms.TextInput(attrs={
			'value': 'Doe',
			'placeholder': 'Insira o nome de seu ultimo nome',
			'oninvalid': "this.setCustomValidity('Por favor insira o apelido aqui')"
		}))
	mother_email = forms.CharField(
		max_length=100,
		widget=forms.TextInput(attrs={
			'value': 'john.doe@portal.co.mz',
			'placeholder': 'Insira o email do pai',
			'oninvalid': "this.setCustomValidity('Por favor insira o email do pai aqui')"
		}))
	mother_ic_number = forms.CharField(
		max_length=13, 
		widget=forms.TextInput(attrs={
			'value': generate_IC(),
			'placeholder': 'Insira o numero de BI',
			'oninvalid': "this.setCustomValidity('Por favor insira o numero de BI aqui')"
		})
	)
	mother_gender = forms.ChoiceField(choices=GENDER)
	# mother_birth_date = forms.DateField(widget=DateInput)
	mother_phone_number = forms.CharField(
	    max_length=13, widget=forms.TextInput(attrs={
		    'value': generate_phone_number(),
			'placeholder': 'Insira o numero de telefone',
			'oninvalid': "this.setCustomValidity('Por favor insira o numero de telefone aqui')"
		}))
	mother_profession = forms.CharField(
		max_length=50, widget=forms.TextInput(attrs={
			'value': 'Medico',
			'placeholder': 'Insira a profissao do pai',
			'oninvalid': "this.setCustomValidity('Por favor insira a cprofissao do pai, aqui')"
		}))
	mother_province = forms.ChoiceField(
		choices=PROVINCE)
	mother_city = forms.CharField(
		max_length=50, widget=forms.TextInput(attrs={
			'value': 'Maputo',
			'placeholder': 'Insira a cidade onde moras',
			'oninvalid': "this.setCustomValidity('Por favor insira a cidade onde moras, aqui')"
		}))
	mother_bairro = forms.CharField(
		max_length=50, widget=forms.TextInput(attrs={
			'value': 'Alto Mae',
			'placeholder': 'Insira o seu bairro',
			'oninvalid': "this.setCustomValidity('Por favor insira o seu bairro aqui')"
		}))


class UpdateTeacherAccountForm(forms.Form):
	GENDER = (
		('masculino', 'Masculino'),
		('feminino', 'Feminino')
	)
	username = forms.CharField(
		max_length=255,
		widget=forms.TextInput(attrs={
			'placeholder': 'Actualize o nome de usuario',
			'oninvalid': "this.setCustomValidity('Por favor actualize nome de usuario aqui')"
		}))
	old_password = forms.CharField(
		max_length=50,
		widget=forms.PasswordInput(attrs={
			'placeholder': 'Escolha a senha',
			'oninvalid': "this.setCustomValidity('Por favor actualize a sua senha aqui')"
		}))
	new_password = forms.CharField(
		max_length=50,
		widget=forms.PasswordInput(attrs={
			'value': 'Jaci1995',
			'placeholder': 'Confirme a sua senha',
			'oninvalid': "this.setCustomValidity('Por favor confirma a sua senha aqui')"
		}))
	new_password_confirm = forms.CharField(
		max_length=50,
		widget=forms.PasswordInput(attrs={
			'value': 'Jaci1995',
			'placeholder': 'Confirme a sua senha',
			'oninvalid': "this.setCustomValidity('Por favor confirma a sua senha aqui')"
		}))



class UpdateStudentForm(forms.Form):
	GENDER = (
		('masculino', 'Masculino'),
		('feminino', 'Feminino')
	)
	email = forms.CharField(
		widget=forms.EmailInput(attrs={
			'placeholder': 'Actualize o seu email aqui',
			'oninvalid': "this.setCustomValidity('Por favor actualize o seu email aqui')"
		}))
	first_name = forms.CharField(
		max_length=100,
		widget=forms.TextInput(attrs={
			'placeholder': 'Actualize o nome de seu primeiro nome',
			'oninvalid': "this.setCustomValidity('Por favor actualize o seu nome aqui')"
		}))
	last_name = forms.CharField(
		max_length=100,
		widget=forms.TextInput(attrs={
			'placeholder': 'Actualize o nome de seu ultimo nome',
			'oninvalid': "this.setCustomValidity('Por favor actualize o apelido aqui')"
		}))
	ic_number = forms.CharField(
		max_length=13, 
		widget=forms.TextInput(attrs={
			'placeholder': 'Actualize o numero de BI',
			'oninvalid': "this.setCustomValidity('Por favor actualize o numero de BI aqui')"
		})
	)
	gender = forms.ChoiceField(choices=GENDER)
	birth_date = forms.DateField(widget=DateInput)
	phone_number = forms.CharField(
	    max_length=13, widget=forms.TextInput(attrs={
			'placeholder': 'Actualize o numero de telefone',
			'oninvalid': "this.setCustomValidity('Por favor actualize o numero de telefone aqui')"
		}))
	profile_pic = forms.ImageField(required=False)
	province = forms.ChoiceField(
		choices=PROVINCE)
	city = forms.CharField(
		max_length=50, widget=forms.TextInput(attrs={
			'placeholder': 'Actualize a cidade onde moras',
			'oninvalid': "this.setCustomValidity('Por favor actualize a cidade onde moras, aqui')"
		}))
	bairro = forms.CharField(
		max_length=50, widget=forms.TextInput(attrs={
			'placeholder': 'Actualize o seu bairro',
			'oninvalid': "this.setCustomValidity('Por favor actualize o seu bairro aqui')"
		}))
	quarteirao = forms.CharField(
		max_length=50,
		required=False,
		widget=forms.TextInput(attrs={
			'placeholder': 'Actualize o quarteirao',
			'oninvalid': "this.setCustomValidity('Por favor actualize o numero de BI aqui')"
		}))


class UpdateTeacherForm(forms.Form):
	GENDER = (
		('masculino', 'Masculino'),
		('feminino', 'Feminino')
	)
	email = forms.CharField(
		widget=forms.EmailInput(attrs={
			'placeholder': 'Actualize o seu email aqui',
			'oninvalid': "this.setCustomValidity('Por favor actualize o seu email aqui')"
		}))
	first_name = forms.CharField(
		max_length=100,
		widget=forms.TextInput(attrs={
			'placeholder': 'Actualize o nome de seu primeiro nome',
			'oninvalid': "this.setCustomValidity('Por favor actualize o seu nome aqui')"
		}))
	last_name = forms.CharField(
		max_length=100,
		widget=forms.TextInput(attrs={
			'placeholder': 'Actualize o nome de seu ultimo nome',
			'oninvalid': "this.setCustomValidity('Por favor actualize o apelido aqui')"
		}))
	ic_number = forms.CharField(
		max_length=13, 
		widget=forms.TextInput(attrs={
			'placeholder': 'Actualize o numero de BI',
			'oninvalid': "this.setCustomValidity('Por favor actualize o numero de BI aqui')"
		})
	)
	gender = forms.ChoiceField(choices=GENDER)
	birth_date = forms.DateField(widget=DateInput)
	phone_number = forms.CharField(
	    max_length=13, widget=forms.TextInput(attrs={
			'placeholder': 'Actualize o numero de telefone',
			'oninvalid': "this.setCustomValidity('Por favor actualize o numero de telefone aqui')"
		}))
	profile_pic = forms.ImageField(required=False)
	province = forms.ChoiceField(
		choices=PROVINCE)
	city = forms.CharField(
		max_length=50, widget=forms.TextInput(attrs={
			'placeholder': 'Actualize a cidade onde moras',
			'oninvalid': "this.setCustomValidity('Por favor actualize a cidade onde moras, aqui')"
		}))
	bairro = forms.CharField(
		max_length=50, widget=forms.TextInput(attrs={
			'placeholder': 'Actualize o seu bairro',
			'oninvalid': "this.setCustomValidity('Por favor actualize o seu bairro aqui')"
		}))
	quarteirao = forms.CharField(
		max_length=50,
		required=False,
		widget=forms.TextInput(attrs={
			'placeholder': 'Actualize o quarteirao',
			'oninvalid': "this.setCustomValidity('Por favor actualize o numero de BI aqui')"
		}))
	university = forms.CharField(
		max_length=50, 
		widget=forms.TextInput(attrs={
			'placeholder': 'Actualize o nome da instituicao onde estudou',
			'oninvalid': "this.setCustomValidity('Por favor actualize o nome da instituicao onde estudou aqui')"
		}))
	degree = forms.ChoiceField(
		choices=NIVEL_ACADEMICO)
	curso = forms.CharField(
		max_length=50, 
		widget=forms.TextInput(attrs={
			'placeholder': 'Actualize o curso pelo qual se formou',
			'oninvalid': "this.setCustomValidity('Por favor actualize o curso pelo qual se formou aqui')"
		}))
	country_of_study = forms.ChoiceField(
		choices=COUNTRIES)
	city_of_study = forms.CharField(
		max_length=50, 
		widget=forms.TextInput(attrs={
			'placeholder': 'Actualize a cidade onde se formou',
			'oninvalid': "this.setCustomValidity('Por favor actualize a cidade onde se formou aqui')"
		}))
	study_start_date = forms.DateField(widget=DateInput)
	study_end_date = forms.DateField(widget=DateInput)



class RegisterTeacherForm(forms.Form):
	GENDER = (
		('masculino', 'Masculino'),
		('feminino', 'Feminino')
	)
	YEARS = ((x, x) for x in range(2023, 2025))
	SEMESTERS = ((semester, semester) for semester in ('Primeiro', 'Segundo', 'Terceiro'))
	CLASSES = ((f'{x}ª classe', f'{x}ª classe') for x in range(8, 13))
	TURMAS = (
		('A', 'A'),
		('B', 'B'),
		('C', 'C')
	)
	username = forms.CharField(
		max_length=255,
		widget=forms.TextInput(attrs={
			'value': 'johndoe',
			'placeholder': 'Insira o nome de usuario',
			'oninvalid': "this.setCustomValidity('Por favor insira nome de usuario aqui')"
		}))
	password = forms.CharField(
		max_length=50,
		widget=forms.PasswordInput(attrs={
			'value': 'Jaci1995',
			'placeholder': 'Escolha a senha',
			'oninvalid': "this.setCustomValidity('Por favor insira a sua senha aqui')"
		}))
	confirm_password = forms.CharField(
		max_length=50,
		widget=forms.PasswordInput(attrs={
			'value': 'Jaci1995',
			'placeholder': 'Confirme a sua senha',
			'oninvalid': "this.setCustomValidity('Por favor confirma a sua senha aqui')"
		}))
	email = forms.CharField(
		widget=forms.EmailInput(attrs={
			# 'value': 'reinata@portal.co.mz',
			'value': 'john.doe@portal.co.mz',
			'placeholder': 'Insira o seu email aqui',
			'oninvalid': "this.setCustomValidity('Por favor insira o seu email aqui')"
		}))
	first_name = forms.CharField(
		max_length=100,
		widget=forms.TextInput(attrs={
			'value': 'Jane',
			'placeholder': 'Insira o nome de seu primeiro nome',
			'oninvalid': "this.setCustomValidity('Por favor insira o seu nome aqui')"
		}))
	last_name = forms.CharField(
		max_length=100,
		widget=forms.TextInput(attrs={
			'value': 'Doe',
			'placeholder': 'Insira o nome de seu ultimo nome',
			'oninvalid': "this.setCustomValidity('Por favor insira o apelido aqui')"
		}))
	ic_number = forms.CharField(
		max_length=13, 
		widget=forms.TextInput(attrs={
			'value': generate_IC(),
			'placeholder': 'Insira o numero de BI',
			'oninvalid': "this.setCustomValidity('Por favor insira o numero de BI aqui')"
		})
	)
	gender = forms.ChoiceField(choices=GENDER)
	quarteirao = forms.CharField(
		max_length=50,
		required=False,
		widget=forms.TextInput(attrs={
			'placeholder': 'Actualize o quarteirao',
			'oninvalid': "this.setCustomValidity('Por favor actualize o numero de BI aqui')"
		}))
	birth_date = forms.DateField(widget=DateInput)
	phone_number = forms.CharField(
	    max_length=13, widget=forms.TextInput(attrs={
		    'value': generate_phone_number(),
			'placeholder': 'Insira o numero de telefone',
			'oninvalid': "this.setCustomValidity('Por favor insira o numero de telefone aqui')"
		}))
	province = forms.ChoiceField(
		choices=PROVINCE)
	city = forms.CharField(
		max_length=50, widget=forms.TextInput(attrs={
			'value': 'Maputo',
			'placeholder': 'Insira a cidade onde moras',
			'oninvalid': "this.setCustomValidity('Por favor insira a cidade onde moras, aqui')"
		}))
	bairro = forms.CharField(
		max_length=50, widget=forms.TextInput(attrs={
			'value': 'Alto Mae',
			'placeholder': 'Insira o seu bairro',
			'oninvalid': "this.setCustomValidity('Por favor insira o seu bairro aqui')"
		}))
	year = forms.ChoiceField(
		choices=YEARS
	)
	semester = forms.ChoiceField(
		choices=SEMESTERS
	)
	classe = forms.ChoiceField(choices=CLASSES)
	turma = forms.ChoiceField(choices=TURMAS)
	university = forms.CharField(
		max_length=50, 
		widget=forms.TextInput(attrs={
			'value': 'Universiti Teknologi Petronas',
			'placeholder': 'Insira o nome da instituicao onde estudou',
			'oninvalid': "this.setCustomValidity('Por favor insira o nome da instituicao onde estudou aqui')"
		}))
	degree = forms.ChoiceField(
		choices=NIVEL_ACADEMICO)
	curso = forms.CharField(
		max_length=50, 
		widget=forms.TextInput(attrs={
			'value': 'Information Technology',
			'placeholder': 'Insira o curso pelo qual se formou',
			'oninvalid': "this.setCustomValidity('Por favor insira o curso pelo qual se formou aqui')"
		}))
	country_of_study = forms.ChoiceField(
		choices=COUNTRIES)
	city_of_study = forms.CharField(
		max_length=50, 
		widget=forms.TextInput(attrs={
			'value': 'Seri Iskendar',
			'placeholder': 'Insira a cidade onde se formou',
			'oninvalid': "this.setCustomValidity('Por favor insira a cidade onde se formou aqui')"
		}))
	study_start_date = forms.DateField(widget=DateInput)
	study_end_date = forms.DateField(widget=DateInput)


class SearchMessageForm(forms.Form):
	date = forms.DateField(widget=DateInput)

class SendMessageForm(forms.Form):
	phone_number = forms.CharField(max_length=13)
	message = forms.CharField(
		max_length=255,
		widget=forms.Textarea(attrs={
			
		})
	)

class SendMessageFormFather(forms.Form):
	father_phone_number = forms.CharField(
		max_length=13, required=False) # , disabled=True)
	father_message = forms.CharField(
		max_length=255,
		required=False,
		widget=forms.Textarea(attrs={
			
		})
	)


class SendMessageFormMother(forms.Form):
	mother_phone_number = forms.CharField(
		max_length=13, required=False) # , disabled=True)
	mother_message = forms.CharField(
		max_length=255,
		required=False,
		widget=forms.Textarea(attrs={
			
		})
	)

class StudentSchoolDetailsForm(forms.Form):
	YEARS = ((x, x) for x in range(2023, 2025))
	year = forms.ChoiceField(
		choices=YEARS
	)


class YearSemesterForm(forms.Form):
	YEARS = ((x, x) for x in range(2023, 2024))
	SEMESTERS = (
        ('Primeiro', 'Primeiro'),
        ('Segundo', 'Segundo'),
        ('Terceiro', 'Terceiro')
    )
	CLASSES = ((f'{x}ª classe', f'{x}ª classe') for x in range(8, 13))
	TURMAS = (
    	('A', 'A'),
    	('B', 'B'),
    	('C', 'C')
    )
	year = forms.ChoiceField(choices=YEARS)
	semester = forms.ChoiceField(choices=SEMESTERS)


class YearSemesterClasseTurmSubjectForm(forms.Form):
	YEARS = ((x, x) for x in range(2023, 2024))
	SEMESTERS = (
        ('Primeiro', 'Primeiro'),
        ('Segundo', 'Segundo'),
        ('Terceiro', 'Terceiro')
    )
	CLASSES = ((f'{x}ª classe', f'{x}ª classe') for x in range(8, 13))
	TURMAS = (
    	('A', 'A'),
    	('B', 'B'),
    	('C', 'C')
    )
	year = forms.ChoiceField(choices=YEARS)
	semester = forms.ChoiceField(choices=SEMESTERS)
	classe = forms.ChoiceField(choices=CLASSES)
	turma = forms.ChoiceField(choices=TURMAS)
	subject = forms.ModelChoiceField(
		queryset=SubjectNameNewModel.objects.all(),
		to_field_name='name',
		required=False,
		widget=forms.Select(attrs={
			'oninvalid': "this.setCustomValidity('Por favor selecione a disciplina')"
		})
	)



class YearSemesterClasseTurmForm(forms.Form):
	YEARS = ((x, x) for x in range(2023, 2024))
	SEMESTERS = (
        ('Primeiro', 'Primeiro'),
        ('Segundo', 'Segundo'),
        ('Terceiro', 'Terceiro')
    )
	CLASSES = ((f'{x}ª classe', f'{x}ª classe') for x in range(8, 13))
	TURMAS = (
    	('A', 'A'),
    	('B', 'B'),
    	('C', 'C')
    )
	year = forms.ChoiceField(choices=YEARS)
	semester = forms.ChoiceField(choices=SEMESTERS)
	classe = forms.ChoiceField(choices=CLASSES)
	turma = forms.ChoiceField(choices=TURMAS)


class StudentStatisticsForms(forms.Form):
    SEMESTERS = (
        ('primeiro', 'Primeiro'),
        ('second', 'Second'),
        ('terceiro', 'Terceiro')
    )
    CLASSES = ((f'{x}ª classe', f'{x}ª classe') for x in range(8, 13))
    TURMAS = (
    	('A', 'A'),
    	('B', 'B'),
    	('C', 'C')
    )
    semester = forms.ChoiceField(choices=SEMESTERS)
    classe = forms.ChoiceField(choices=CLASSES)
    turma = forms.ChoiceField(choices=TURMAS)

class UserForm(forms.Form):
	username = forms.CharField(
		max_length=255,
		widget=forms.TextInput(attrs={
			'value': 'reinata',
			'placeholder': 'Insira o nome de usuario',
			'oninvalid': "this.setCustomValidity('Por favor insira nome de usuario aqui')"
		}))
	first_name = forms.CharField(
		max_length=100,
		widget=forms.TextInput(attrs={
			'value': 'Monica',
			'placeholder': 'Insira o nome de seu primeiro nome',
			'oninvalid': "this.setCustomValidity('Por favor insira o seu nome aqui')"
		}))
	last_name = forms.CharField(
		max_length=100,
		widget=forms.TextInput(attrs={
			'value': 'Cabir',
			'placeholder': 'Insira o nome de seu ultimo nome',
			'oninvalid': "this.setCustomValidity('Por favor insira o apelido aqui')"
		}))
	email = forms.EmailField(
		widget=forms.EmailInput(attrs={
			'value': 'reinata@portal.co.mz',
			'placeholder': 'Insira o nome de seu email',
			'oninvalid': "this.setCustomValidity('Por favor insira o seu email aqui')"
		}))
	password = forms.CharField(
		max_length=50,
		widget=forms.PasswordInput(attrs={
			'value': 'Jaci1995',
			'placeholder': 'Escolha a senha',
			'oninvalid': "this.setCustomValidity('Por favor insira a sua senha aqui')"
		}))
	confirm_password = forms.CharField(
		max_length=50,
		widget=forms.PasswordInput(attrs={
			'value': 'Jaci1995',
			'placeholder': 'Confirme a sua senha',
			'oninvalid': "this.setCustomValidity('Por favor confirma a sua senha aqui')"
		}))
	phone_number = forms.CharField(
		max_length=50,
		widget=forms.TextInput(attrs={
			'value': '869643215',
			'placeholder': 'Insira o nome de seu numero de telemovel',
			'oninvalid': "this.setCustomValidity('Por favor insira o seu numero de telefone')"
		}))
	location = forms.CharField(
		max_length=100,
		widget=forms.TextInput(attrs={
			'value': 'Maputo',
			'placeholder': 'Insira o seu endereco',
			'oninvalid': "this.setCustomValidity('Por favor insira o seu endereco')"
		}))
	# privince = forms.CharField(
	# 	max_length=100,
	# 	widget=forms.TextInput(attrs={
	# 		'value': 'Maputo',
	# 		'placeholder': 'Insira a sua provincia aqui',
	# 		'oninvalid': "this.setCustomValidity('Por favor insira a sua provincia aqui')"
	# 	}))
	# city = forms.CharField(
	# 	max_length=100,
	# 	widget=forms.TextInput(attrs={
	# 		'value': 'Maputo',
	# 		'placeholder': 'Insira a sua cidade',
	# 		'oninvalid': "this.setCustomValidity('Por favor insira a sua cidade aqui')"
	# 	}))


class LoginForm(forms.Form):
	username = forms.CharField(max_length=255)
	password = forms.CharField(
		max_length=50,
		widget=forms.PasswordInput)

class SearchStudentForm(forms.Form):
	first_name = forms.CharField(
		max_length=100,
		required=False,
		widget=forms.TextInput(attrs={
			# 'value': 'Angela',
			'placeholder': 'Insira o primeiro nome',
			'oninvalid': "this.setCustomValidity('Por favor insira o primeiro nome aqui')"
		}))
	last_name = forms.CharField(
		max_length=100,
		required=False,
		widget=forms.TextInput(attrs={
			'value': 'Williams',
			'placeholder': 'Insira o ultimo nome',
			'oninvalid': "this.setCustomValidity('Por favor insira o ultimo nome aqui')"
		}))
	# CHOICES = ((f'{x}ª classe', f'{x}ª Classe') for x in range(12, 7, -1))
	# classe = forms.ChoiceField(choices=CHOICES)


class StudentAttendanceForm(forms.Form):
	YEARS = ((x, x) for x in range(2023, 2024))
	TURMAS = (
		('A', 'A'),
		('B', 'B')
	)
	CLASSES = ((f'{x}ª classe', f'{x}ª Classe') for x in range(8, 13))
	SEMESTERS = ((semester, semester) for semester in ('Primeiro', 'Segundo', 'Terceiro'))
	year = forms.ChoiceField(
		choices=YEARS
	)

	semester = forms.ChoiceField(
		choices=SEMESTERS
	)
	classe = forms.ChoiceField(choices=CLASSES)
	turma = forms.ChoiceField(
		choices=TURMAS
	)
	# month = forms.DateField(widget=MonthInput)
	month = forms.ChoiceField(
		choices=MONTHS
	)


def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.pdf', '.doc', '.docx', '.jpg', '.png', '.xlsx', '.xls']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension.')

class AddStudentMarkFromFileForm(forms.Form):
	YEARS = ((x, x) for x in range(2023, 2024))
	TURMAS = (
		('A', 'A'),
		('B', 'B')
	)
	CLASSES = ((f'{x}ª classe', f'{x}ª Classe') for x in range(8, 13))
	SEMESTERS = ((semester, semester) for semester in ('Primeiro', 'Segundo', 'Terceiro'))
	TESTS = ((f'Test {x}', f'Test {x}') for x in range(1, 4))
	year = forms.ChoiceField(
		choices=YEARS
	)

	semester = forms.ChoiceField(
		choices=SEMESTERS
	)
	classe = forms.ChoiceField(choices=CLASSES)
	turma = forms.ChoiceField(
		choices=TURMAS
	)
	subject = forms.ModelChoiceField(
		queryset=SubjectNameNewModel.objects.all(),
		to_field_name='name',
		required=False,
		widget=forms.Select(attrs={
			'oninvalid': "this.setCustomValidity('Por favor selecione a disciplina')"
		})
	)
	test = forms.ChoiceField(choices=TESTS)
	file = forms.FileField(
		required=False,
		validators=[FileExtensionValidator(
			allowed_extensions=['xlsx', 'csv'])],
		widget=forms.FileInput(attrs={
			'oninvalid': "this.setCustomValidity('Por favor selecione o ficheiro')"
		})
	)


class StudentAllMarkForm(forms.Form):
	YEARS = ((x, x) for x in range(2023, 2024))
	TURMAS = (
		('A', 'A'),
		('B', 'B')
	)
	CLASSES = ((f'{x}ª classe', f'{x}ª Classe') for x in range(8, 13))
	SEMESTERS = ((semester, semester) for semester in ('Primeiro', 'Segundo', 'Terceiro'))
	year = forms.ChoiceField(
		choices=YEARS
	)

	semester = forms.ChoiceField(
		choices=SEMESTERS
	)
	classe = forms.ChoiceField(choices=CLASSES)
	turma = forms.ChoiceField(
		choices=TURMAS
	)


class StudentMarkForm(forms.Form):
	YEARS = ((x, x) for x in range(2023, 2024))
	TURMAS = (
		('A', 'A'),
		('B', 'B')
	)
	CLASSES = ((f'{x}ª classe', f'{x}ª Classe') for x in range(8, 13))
	SEMESTERS = ((semester, semester) for semester in ('Primeiro', 'Segundo', 'Terceiro'))
	year = forms.ChoiceField(
		choices=YEARS
	)

	semester = forms.ChoiceField(
		choices=SEMESTERS
	)
	classe = forms.ChoiceField(choices=CLASSES)
	turma = forms.ChoiceField(
		choices=TURMAS
	)
	subject = forms.ModelChoiceField(
        queryset=SubjectNameNewModel.objects.all(),
        to_field_name='name',
        required=False,  
        widget=forms.Select(attrs={
			'class': 'form-control',
			'oninvalid': "this.setCustomValidity('Por favor selecione a disciplina')"
		})
	)

class AddStudentMarkForm(forms.Form):
	YEARS = ((x, x) for x in range(2023, 2024))
	TURMAS = (
		('A', 'A'),
		('B', 'B')
	)
	CLASSES = ((f'{x}ª classe', f'{x}ª Classe') for x in range(8, 13))
	SEMESTERS = ((semester, semester) for semester in ('Primeiro', 'Segundo', 'Terceiro'))
	year = forms.ChoiceField(
		choices=YEARS
	)

	semester = forms.ChoiceField(
		choices=SEMESTERS
	)
	classe = forms.ChoiceField(choices=CLASSES)
	turma = forms.ChoiceField(
		choices=TURMAS
	)
	# subject = forms.ModelChoiceField(
    #     queryset=SubjectNameNewModel.objects.all(),
    #     to_field_name='name',
    #     required=False,  
    #     widget=forms.Select(attrs={'class': 'form-control'})
	# )


class AttentanceForm(forms.Form):
	YEARS = ((x, x) for x in range(2023, 2024))
	TURMAS = (
		('A', 'A'),
		('B', 'B')
	)
	CLASSES = ((f'{x}ª classe', f'{x}ª Classe') for x in range(8, 13))
	SEMESTERS = ((semester, semester) for semester in ('Primeiro', 'Segundo', 'Terceiro'))
	year = forms.ChoiceField(
		choices=YEARS
	)
	semester = forms.ChoiceField(
		choices=SEMESTERS
	)
	classe = forms.ChoiceField(choices=CLASSES)
	turma = forms.ChoiceField(
		choices=TURMAS
	)
	subject = forms.ModelChoiceField(
        queryset=SubjectNameNewModel.objects.all(),
        to_field_name='name',
        required=False,  
        widget=forms.Select(attrs={'class': 'form-control'})
	)


class TimeTableForm(forms.Form):
	YEARS = ((x, x) for x in range(2023, 2024))
	TURMAS = (
		('A', 'A'),
		('B', 'B')
	)
	CLASSES = ((f'{x}ª classe', f'{x}ª Classe') for x in range(8, 13))
	SEMESTERS = ((semester, semester) for semester in ('Primeiro', 'Segundo', 'Terceiro'))
	year = forms.ChoiceField(
		choices=YEARS
	)

	semester = forms.ChoiceField(
		choices=SEMESTERS
	)
	classe = forms.ChoiceField(choices=CLASSES)
	turma = forms.ChoiceField(
		choices=TURMAS
	)


class TeacherAttendanceForm(forms.Form):
	YEARS = ((x, x) for x in range(2023, 2025))
	TURMAS = (
		('A', 'A'),
		('B', 'B')
	)
	CLASSES = ((f'{x}ª classe', f'{x}ª Classe') for x in range(8, 13))
	SEMESTERS = ((semester, semester) for semester in ('Primeiro', 'Segundo', 'Terceiro'))
	year = forms.ChoiceField(
		choices=YEARS
	)

	semester = forms.ChoiceField(
		choices=SEMESTERS
	)
	classe = forms.ChoiceField(choices=CLASSES)
	turma = forms.ChoiceField(
		choices=TURMAS
	)
	month = forms.ChoiceField(
		choices=MONTHS
	)



class CheckTeacherForm(forms.Form):
	YEARS = ((x, x) for x in range(2023, 2025))
	TURMAS = (
		('A', 'A'),
		('B', 'B')
	)
	# CLASSES = ((f'{x}ª classe', f'{x}ª Classe') for x in range(12, 7, -1))
	CLASSES = ((f'{x}ª classe', f'{x}ª Classe') for x in range(8, 13))
	SEMESTERS = ((semester, semester) for semester in ('Primeiro', 'Segundo', 'Terceiro'))
	year = forms.ChoiceField(
		choices=YEARS
	)

	semester = forms.ChoiceField(
		choices=SEMESTERS
	)
	classe = forms.ChoiceField(choices=CLASSES)

	turma = forms.ChoiceField(
		choices=TURMAS
	)
	gender = forms.ChoiceField(
		choices=GENDER
	)
