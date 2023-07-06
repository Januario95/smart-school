from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from app2.models import (
	SubjectName, SubjectMark, Turma, Classe, Test,
	Student, Teacher, Parent, Semester
)
from app2.models import (
    SemesterNewModel, ClasseNewModel, TurmaNewModel,
    TestNewModel, StudentNameNewModel, SubjectNewModel,
    SubjectNameNewModel, Year, SemesterModel, SubjectTestsNewModel,
    ParentNameNewModel, TeacherNameNewModel, Attendance,
    AdminToParentsMessage
)


import json
import string
import random
import pandas as pd
import datetime as dt
from faker import Faker

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

class Command(BaseCommand):
	help = 'Generate random data to the database'

	def handle(self, *args, **options):
		faker = Faker()
		GENDER = ('male', 'female')
		BAIRROS = ['Polana Cimento', 'Aeroporto', 'Polana Canico A',
				  'Maxaquene A', 'Maxaquene B', 'Somershild', 'Bairro Central',
				  'Zimpeto', 'Museu']
		TEST_NAMES = ['test1', 'test2', 'test3']
		SUBJECT_NAMES = ['Ingles', 'Portugues', 'Biologia', 'Quimica', 'Fisica', 'Matematica']
		CLASSES = ['8ª classe', '9ª classe', '10ª classe', '11ª classe', '12ª classe']
		SEMESTERS = ['Primeiro', 'Segundo', 'Terceiro']



		# admin = User.objects.first()
		# # print(admin.is_superuser)

		# father = ParentNameNewModel.objects.get(phone_number='+258820255368')
		# print(father)
		# message = AdminToParentsMessage.objects.create(
		# 	sender=father,
		# 	receiver=admin,
		# 	message='Bom dia Director'
		# )
		# message.save()
		# print(message)

		# mother = ParentNameNewModel.objects.get(phone_number='+258844584472')
		# print(mother)
		# message = AdminToParentsMessage.objects.create(
		# 	sender=mother,
		# 	receiver=admin,
		# 	message='Bom dia Sr Director'
		# )
		# message.save()
		# print(message)

		# parents = ParentNameNewModel.objects.all()
		# for parent in parents:
		# 	parent.email = parent.first_name.lower() + '.' + parent.last_name.lower() + '@portal.co.mz' # email.lower()
		# 	parent.save()
		# 	print(f'{parent!r} updated email')

		# students = StudentNameNewModel.objects.all()
		# for stud in students:
		# 	stud.email = stud.first_name.lower() + '.' + stud.last_name.lower() + '@portal.co.mz' # email.lower()
		# 	stud.save()
		# 	print(f'{stud!r} updated email')

		# attendances = Attendance.objects.all()
		# index = 3
		# for attendance in attendances:
		# 	class_time=dt.datetime(2023, 6, index, random.choice([8, 13, 15]), 
		# 	    						   random.choice([0, 25, 30, 45]))
		# 	print(attendance.class_time)
		# 	attendance.class_time = class_time
		# 	attendance.save()
		# 	index += 1
		# 	print(attendance.class_time)


		# semester_name = SemesterNewModel.objects.get(name='Terceiro')
		# new_semester = SemesterModel.objects.filter(
		# 	name=semester_name
		# )
		# students = StudentNameNewModel.objects.filter(new_semester__in=new_semester)
		# for student in students:
		# 	semester = new_semester.first()
		# 	student.new_semester.remove(semester)
		# 	student.save()
		# 	print(f'{semester} removed from {student}')
		# for sem in new_semester:
		# 	sem.delete()


		# students_ = []
		# year = Year.objects.get(year='2023')
		# turma = TurmaNewModel.objects.get(name='A')
		# classe = ClasseNewModel.objects.get(name='8ª classe')
		# # semester_name = SemesterNewModel.objects.get(name=semester_name)
		# new_semester = SemesterModel.objects.filter(
		# 	# name=semester_name,
		# 	turma=turma,
		# 	classe=classe,
		# 	year=year
		# )
		# students = StudentNameNewModel.objects.filter(new_semester__in=new_semester)
		# print(students.count())
		# for student in students:
		# 	print(student)

		# year = Year.objects.get(year='2023')
		# for turma in ['A', 'B']:
		# 	for semester_name in ['Primeiro', 'Segundo']:
		# 		for x in range(8, 13):
		# 			turma = TurmaNewModel.objects.get(name=turma)
		# 			classe = ClasseNewModel.objects.get(name=f'{x}ª classe')
		# 			# semester_name = SemesterNewModel.objects.get(name=semester_name)

		# 			new_semester = SemesterModel.objects.filter(
		# 				# name=semester_name,
		# 				turma=turma,
		# 				classe=classe,
		# 				year=year
		# 			)
					
		# 			students = StudentNameNewModel.objects.filter(
		# 					new_semester__in=new_semester
		# 			)
		# 			for index, student in enumerate(students, start=1):
		# 				if index > 25:
		# 					student.delete()
		# 			print(students.count())
					# semester_name = SemesterNewModel.objects.get(name='Terceiro')
					# for student in students:
					# 	new_semester = SemesterModel.objects.create(
					# 		name=semester_name,
					# 		turma=turma,
					# 		classe=classe,
					# 		year=year
					# 	)
					# 	print(new_semester)
					# 	student.new_semester.add(new_semester)
					# print(students.count())



		# new_semester = new_semester.first()
		# print(new_semester.subjects.all())
		# teachers = TeacherNameNewModel.objects.all()
		# for teacher in teachers:
		# 	teacher.email = teacher.first_name.lower() + '.' + teacher.last_name.lower() + '@portal.co.mz'
		# 	teacher.save()
		# for subject_name, teacher in zip(SUBJECT_NAMES, teachers):
			# semester = SemesterModel.objects.create(
			# 	name=semester_name,
			# 	turma=turma,
			# 	classe=classe,
			# 	year=year
			# )
			# semester.save()
			# subject = SubjectTestsNewModel.objects.create(
			# 	name=SubjectNameNewModel.objects.get(name=subject_name)
			# )
			# subject.save()
			# semester.subjects.add(subject)
			# semester.delete()
			# subject.delete()
			# teacher.new_semester.remove(new_semester)
			# teacher.new_semester.add(semester)
			# teacher.save()
			# print(f'Added {semester!r} to teachre {teacher!r}')

		# print(students.count())

		# year = Year.objects.get(year='2023')
		# turma = TurmaNewModel.objects.get(name='B')
		# classe = ClasseNewModel.objects.get(name='11ª classe')
		# semester_name = SemesterNewModel.objects.get(name='Primeiro')
		# new_semester = SemesterModel.objects.filter(
		# 	name=semester_name, year=year, turma=turma, classe=classe, 
		# )
		# print(new_semester.count())
		# students = StudentNameNewModel.objects.filter(new_semester__in=new_semester)
		# print(students.count())
		teachers = TeacherNameNewModel.objects.all()
		# print(teachers.count())
		# for teacher in teachers:
		# 	teacher.email = teacher.email.lower()
		# 	teacher.save()


		students = StudentNameNewModel.objects.all()
		for student in students:
			student.email = student.email.lower()
			student.save()

		
		# for index, value in enumerate(zip(SUBJECT_NAMES, teachers[6:12]), start=3):
		# 	subject_name, teacher = value
		# 	subject=SubjectNameNewModel.objects.get(name=subject_name)

		# 	sem = new_semester.first()
		# 	teacher.new_semester.add(sem)
		# 	teacher.save()
		# 	print(f'Semester {sem} added to {teacher}')


		# for index, subject_name in enumerate(SUBJECT_NAMES, start=1):
		# 	year = Year.objects.get(year='2023')
		# 	turma = TurmaNewModel.objects.get(name='A')
		# 	classe = ClasseNewModel.objects.get(name='8ª classe')
		# 	semester_name = SemesterNewModel.objects.get(name='Primeiro')
		# 	subject=SubjectNameNewModel.objects.get(name=subject_name)
		# 	new_semester_ = SemesterModel.objects.create(
		# 		name=semester_name, year=year, turma=turma, classe=classe, 
		# 	)
		# 	new_semester_.save()
		
		# 	first_name = faker.first_name()
		# 	last_name = faker.last_name()
		# 	teacher = TeacherNameNewModel.objects.create(
		# 		first_name=first_name,
		# 		last_name=last_name,
		# 		numero_de_bi=generate_IC(),
		# 		gender=random.choice(GENDER),
		# 		birth_date=dt.date(random.randint(1990, 2000),
		# 						   random.randint(1, 12),
		# 						   random.randint(1, 28)),
		# 		phone_number=generate_phone_number(),
		# 		email=first_name + '.' + last_name + '@portal.co.mz',
		# 		province='Maputo Cidade',
		# 		city='Maputo',
		# 		bairro=random.choice(BAIRROS),
		# 	)
		# 	teacher.save()
		# 	gender = teacher.gender
		# 	if gender == 'male':
		# 		first_name = faker.first_name_male()
		# 	else:
		# 		first_name = faker.first_name_female()
		# 	teacher.first_name = first_name
		# 	teacher.save()

		# 	subject_test = SubjectTestsNewModel.objects.create(name=subject)
		# 	new_semester_.subjects.add(subject_test)
		# 	teacher.new_semester.add(new_semester_)
		# 	subject_test.save()
		# 	print(f'Teacher {teacher!r} created')
			
			# for student in students:
			# 	attendance = Attendance.objects.create(
			# 		teacher=teacher,
			# 		student=student,
			# 		subject=subject,
			# 		# semester=new_semester,
			# 		semester=new_semester.first(),
			# 		is_present=random.choice([True, False]),
			# 		class_time=dt.datetime(2023, 6, index, random.choice([8, 13, 15]), 
			#     						   random.choice([0, 25, 30, 45]))
			# 	)
			# 	attendance.save()
			# 	print(attendance)


		# year = Year.objects.get(year='2023')
		# turma = TurmaNewModel.objects.get(name='B')
		# classe = ClasseNewModel.objects.get(name='12ª classe')
		# semester_name = SemesterNewModel.objects.get(name='Terceiro')
		# new_semester = SemesterModel.objects.filter(
		# 	name=semester_name,
		# 	turma=turma,
		# 	classe=classe,
		# 	year=year
		# )
		# # print(new_semester)
		# students = StudentNameNewModel.objects.filter(new_semester__in=new_semester)
		# print(students)


		# teachers = TeacherNameNewModel.objects.all()
		# for teacher in teachers:
		# 	stud_semesters = teacher.new_semester.all()
		# 	for sem in stud_semesters:
		# 		sem.user_type = 'teacher'
		# 		sem.save()
		# 	# print(teacher.pk)
		# 	year = Year.objects.get(year='2023')
		# 	turma = TurmaNewModel.objects.get(name='B')
		# 	classe = ClasseNewModel.objects.get(name='12ª classe')
		# 	semester_name = SemesterNewModel.objects.get(name='Terceiro')
		# 	new_semester = SemesterModel.objects.create(
		# 		name=semester_name,
		# 		turma=turma,
		# 		classe=classe,
		# 		year=year
		# 	)
		# 	teacher.new_semester.add(new_semester)
			# teacher.save()
		# 	print(f'{semester_name!r} added to teacher {teacher!r}')
			
			

		# for turma in ['A', 'B']:
		# 	for semester_name in ['Primeiro', 'Segundo']:
		# 		year = Year.objects.get(year='2023')
		# 		turma = TurmaNewModel.objects.get(name=turma)
		# 		classe = ClasseNewModel.objects.get(name='12ª classe')
		# 		semester_name = SemesterNewModel.objects.get(name=semester_name)
		# 		semester = SemesterModel.objects.filter(
		# 			name=semester_name,
		# 			turma=turma,
		# 			classe=classe,
		# 			year=year
		# 		)
		# 		students = StudentNameNewModel.objects.filter(new_semester__in=semester)
		# 		print(f'Turma {turma}, Semestre {semester_name}')
		# 		print(students.count())
		# 		print([student.fullname() for student in students])
		# 		print()
	



		# for subject_name in SUBJECT_NAMES:
		# 	year = Year.objects.get(year='2023')
		# 	turma = TurmaNewModel.objects.get(name='A')
		# 	classe = ClasseNewModel.objects.get(name='12ª classe')
		# 	semester_name = SemesterNewModel.objects.get(name='Primeiro')
		# 	new_semester = SemesterModel.objects.create(
		# 		name=semester_name,
		# 		turma=turma,
		# 		classe=classe,
		# 		year=year
		# 	)
		# 	# print(new_semester.first())

		# 	subjects = SubjectTestsNewModel.objects.filter(
		# 		name=SubjectNameNewModel.objects.get(name=subject_name),
		# 	)
		# 	subject = subjects.first()
		# 	print(subject)
		# 	new_semester.subjects.add(subject)

		# 	gender = random.choice(GENDER)
		# 	if gender == 'male':
		# 		first_name = faker.first_name_male()
		# 	else:
		# 		first_name = faker.first_name_female()

		# 	last_name = faker.last_name()
			
		# 	teacher = TeacherNameNewModel.objects.create(
		# 		first_name=first_name,
		# 		last_name=last_name,
		# 		numero_de_bi=generate_IC(),
		# 		gender=gender,
		# 		birth_date=dt.date(random.randint(1990, 2000),
		# 						   random.randint(1, 12),
		# 						   random.randint(1, 28)),
		# 		phone_number=generate_phone_number(),
		# 		email=first_name + '.' + last_name + '@portal.co.mz',
		# 		province='Maputo Cidade',
		# 		city='Maputo',
		# 		bairro=random.choice(BAIRROS),
		# 	)
		# 	teacher.new_semester.add(new_semester)
		# 	teacher.save()
		# 	print(f'Created teacher {teacher!r}')



		# students = StudentNameNewModel.objects.all()
		# for student in students:
		# 	stud_semesters = student.new_semester.all()
		# 	for sem in stud_semesters:
		# 		sem.user_type = 'student'
		# 		sem.save()
			# if student.gender == 'male':
			# 	student.first_name = faker.first_name_male()
			# if student.gender == 'female':
			# 	student.first_name = faker.first_name_female()
			# student.save()
			# print(f'Updating {student}')
			# student.save()
		


		# year = Year.objects.get(year='2022')
		# turma = TurmaNewModel.objects.get(name='A')
		# classe = ClasseNewModel.objects.get(name='8ª classe')
		# new_semester = SemesterModel.objects.filter(
		# 	year=year, turma=turma, classe=classe
		# )
		# print(new_semester.count())



		# for index in range(25):
		# 	first_name = faker.first_name()
		# 	last_name = faker.last_name()

		# 	student = StudentNameNewModel.objects.create(
		# 		first_name=first_name,
		# 		last_name=last_name,
		# 		numero_de_bi=generate_IC(),
		# 		gender=random.choice(GENDER),
		# 		birth_date=dt.date(random.randint(2002, 2007),
		# 						   random.randint(1, 12),
		# 						   random.randint(1, 28)),
		# 		phone_number=generate_phone_number(),
		# 		email=first_name + '.' + last_name + '@portal.co.mz',
		# 		province='Maputo Cidade',
		# 		city='Maputo',
		# 		bairro=random.choice(BAIRROS),
		# 	)
		# 	student.save()
		# 	print(f'Created student {student!r}')


		# 	year = Year.objects.get(year='2022')
		# 	turma = TurmaNewModel.objects.get(name='B')
		# 	classe = ClasseNewModel.objects.get(name='12ª classe')
		# 	for semester_name in ['Primeiro', 'Segundo', 'Terceiro']:
		# 		semester = SemesterNewModel.objects.get(name=semester_name)
		# 		new_semester = SemesterModel.objects.create(
		# 			name=semester,
		# 			turma=turma,
		# 			classe=classe,
		# 			year=year
		# 		)
		# 		new_semester.save()
		# 		for subject_name in SUBJECT_NAMES:
		# 			subject = SubjectTestsNewModel.objects.create(
		# 				name=SubjectNameNewModel.objects.get(name=subject_name),
		# 			)
		# 			subject.save()
		# 			# print(f'Created subject {subject!r}')
		# 			for index in range(1, 4):
		# 				test = TestNewModel.objects.create(
		# 					name=f'Test {index}', mark=random.randint(6, 19) + round(random.random(), 1))
		# 				test.save()
		# 				# print(f'Created test {test!r}')
		# 				subject.tests.add(test)
		# 				# print(f'Test added to subject {subject!r}')
		# 				subject.save()
		# 			new_semester.subjects.add(subject)
		# 			new_semester.save()
		# 			# print(f'Added subject {subject!r} to student {student!r}')
		# 			# print('')
		# 		student.new_semester.add(new_semester)





			
		
		# year = Year.objects.get(year='2023')
		# turma = TurmaNewModel.objects.get(name='B')
		# classe = ClasseNewModel.objects.get(name='12ª classe')
		# semester_name = SemesterNewModel.objects.get(name='Primeiro')
		# students = StudentNameNewModel.objects.filter(year=year, semester=semester_name,
		# 				  							  classe=classe, turma=turma)
		
		# new_semester = SemesterModel.objects.filter(
		# 	name=semester_name,
		# 	turma=turma,
		# 	classe=classe,
		# 	year=year
		# )
		# # print(new_semester)
		# students = StudentNameNewModel.objects.filter(
		# 		new_semester__in=new_semester
		# )
		# print(students.count())
		# # year = Year.objects.get(year='2023')
		# # turma = TurmaNewModel.objects.get(name='A')
		# # classe = ClasseNewModel.objects.get(name='8ª classe')
		# semester_name = SemesterNewModel.objects.get(name='Segundo')
		# for student in students:
		# 	new_semester = SemesterModel.objects.create(
		# 		name=semester_name,
		# 		turma=turma,
		# 		classe=classe,
		# 		year=year
		# 	)
		# 	new_semester.save()
		# 	for subject_name in SUBJECT_NAMES:
		# 		subject = SubjectTestsNewModel.objects.create(
		# 			name=SubjectNameNewModel.objects.get(name=subject_name),
		# 		)
		# 		subject.save()
		# 		print(f'Created subject {subject!r}')
		# 		for index in range(1, 4):
		# 			test = TestNewModel.objects.create(
		# 				name=f'Test {index}', mark=random.randint(6, 19) + round(random.random(), 1))
		# 			test.save()
		# 			print(f'Created test {test!r}')
		# 			subject.tests.add(test)
		# 			print(f'Test added to subject {subject!r}')
		# 			subject.save()
		# 		new_semester.subjects.add(subject)
		# 		new_semester.save()
		# 		print(f'Added subject {subject!r} to student {student!r}')
		# 		print('')
		# 	student.new_semester.add(new_semester)


			# if student.gender == 'male':
			# 	student.first_name = faker.first_name_male()
			# if student.gender == 'female':
			# 	student.first_name = faker.first_name_female()
			# student.save()
			# print(f'{student!r} gender changed to {student.gender!r}')



			# parents = student.parents.all()
			# for parent in parents:
			# 	parent.job_title = faker.job()
			# 	parent.save()
			# 	print(f'Generate job_title {parent.job_title!r} for parent {parent!r}')


			# student.last_name = faker.last_name_male()
			# faker.gender = random.choice(GENDER)
			# student.save()
	

		# students = StudentNameNewModel.objects.all()
		# for student in students:

		# 	father_last_name = faker.last_name_male()
		# 	father = ParentNameNewModel.objects.create(
		# 		first_name=student.last_name,
		# 		last_name=father_last_name,
		# 		gender='male',
		# 		phone_number=generate_phone_number(),
		# 		email=student.last_name + '.' + father_last_name + '@portal.co.mz',
		# 		province=student.province,
		# 		city=student.city,
		# 		bairro=student.bairro
		# 	)
		# 	father.save()
		# 	print(f'Created father {father!r} for student {student!r}')
			
		# 	mother_first_name = faker.first_name_female()
		# 	mother_last_name = faker.last_name()
		# 	mother = ParentNameNewModel.objects.create(
		# 		first_name=mother_first_name,
		# 		last_name=mother_last_name,
		# 		gender='female',
		# 		phone_number=generate_phone_number(),
		# 		email=mother_first_name + '.' + mother_last_name + '@portal.co.mz',
		# 		province=student.province,
		# 		city=student.city,
		# 		bairro=student.bairro
		# 	)
		# 	mother.save()
		# 	print(f'Created mother {father!r} for student {student!r}')
		# 	student.parents.add(father)
		# 	student.parents.add(mother)
		# 	student.save()
		# 	print(f'Added father and mother for student {student!r}')





		# for index in range(25):
		# 	first_name = faker.first_name()
		# 	last_name = faker.last_name()

			# turma = TurmaNewModel.objects.get(name='B')
			# classe = ClasseNewModel.objects.get(name='12ª classe')
			# semester = SemesterNewModel.objects.get(name='Primeiro')
			
			# student = StudentNameNewModel.objects.create(
			# 	first_name=first_name,
			# 	last_name=last_name,
			# 	numero_de_bi=generate_IC(),
			# 	gender=random.choice(GENDER),
			# 	birth_date=dt.date(random.randint(2002, 2008),
			# 					   random.randint(1, 12),
			# 					   random.randint(1, 28)),
			# 	phone_number=generate_phone_number(),
			# 	email=first_name + '.' + last_name + '@portal.co.mz',
			# 	province='Maputo Cidade',
			# 	city='Maputo',
			# 	bairro=random.choice(BAIRROS)
			# )
			# student.year.add(year)
			# student.save()
			# print(f'Created student {student!r}')

			# stud.year.add(year)
			# stud.birth_date = dt.date(random.randint(2002, 2008),
			#      					  random.randint(1, 12),
			# 						  random.randint(1, 28))
			# stud.email = stud.email.lower()
			# stud.save()
			# print(f'Updated birth_date {stud.birth_date!r} for student {stud!r}')














		# turmas = ['A', 'B']
		# for turma in turmas:
		# 	classes = [f'{x}ª classe' for x in range(8, 13)]
		# 	for class_name in classes:
		# 		print(class_name)
		# 		turma = Turma.objects.get(name=turma)
		# 		clss = Classe.objects.get(name=class_name, turma=turma)
		# 		semester = Semester.objects.get(
		# 			classe=clss)
		# 		print(semester)
		# 		teachers = Student.objects.filter(
		# 			classe=clss)
		# 		for teacher in teachers:
		# 			# if semester.exists:
		# 			semester = semester
		# 			try:
		# 				teacher.semester = semester
		# 				print(teacher.semester)
		# 				teacher.save()
		# 			except Exception as e:
		# 				print(e)
		# 			print('Teacher registered successfully')




		# turma = Turma.objects.get(name='B')
		# clss = Classe.objects.get(name='8ª classe', turma=turma)
		# semester = Semester.objects.get(
		# 	classe=clss)
		# print(semester)
		# students = Student.objects.filter(
		# 	classe=clss)
		# for student in students:
		# 	# if semester.exists:
		# 	semester = semester
		# 	student.semester = semester
		# 	student.save()
		# 	print('Student registered successfully')



		# students = Student.objects.all()
		# for index, stud in enumerate(students, start=1):
		# 	username = stud.first_name.lower() + stud.last_name.lower()
		# 	try:
		# 		user = User.objects.get(username=username)
		# 		print(f'Student: {stud} = {user.is_staff}')
				# user = User.objects.create(
				# 	username=username
				# )
				# user.set_password('Jaci1995')
				# user.save()
				# print(f'{username} for student created successfully')
			# except Exception as e:
			# 	print(e.args)
			# print(f'INDEX={index}')

		# teachers = Teacher.objects.all()
		# semesters = Semester.objects.all()
		# for index, teacher in enumerate(teachers, start=1):
		# 	# username = teacher.first_name.lower() + teacher.last_name.lower()
		# 	semester = random.choice(semesters)
		# 	teacher.semester = semester
		# 	teacher.save()
		# 	print(f'Semester successfully added')
			# try:
			# 	user = User.objects.get(username=username)
			# 	user.first_name = teacher.first_name
			# 	user.last_name = teacher.last_name
			# 	# user.is_staff = True
			# 	# user.save()
			# 	print(f'Teacher: {teacher} = {user.is_staff}')
			# 	# user = User.objects.create(
			# 	# 	username=username
			# 	# )
			# 	# user.set_password('Jaci1995')
			# 	user.save()
			# 	# print(f'{username} for teacher created successfully')
			# except Exception as e:
			# 	print(e.args)
			# print(f'INDEX={index}')





		# students = Student.objects.all()
		# for stud in students:
		# 	obj = Parent.objects.create(
		# 		first_name=stud.last_name,
		# 		last_name=faker.last_name_male(),
		# 		email=faker.email(),
		# 		job_title=faker.job(),
		# 		phone_number=generate_phone_number(),
		# 		gender=random.choice(GENDER),
		# 		province='Maputo Province',
		# 		city='Maputo',
		# 		bairro=random.choice(BAIRROS),
		# 		quarteirao='A',
		# 		is_male=True
		# 	)
		# 	obj.save()
		# 	stud.parents.add(obj)

		# 	obj = Parent.objects.create(
		# 		first_name=faker.first_name_female(),
		# 		last_name=faker.last_name_female(),
		# 		email=faker.email(),
		# 		job_title=faker.job(),
		# 		phone_number=generate_phone_number(),
		# 		gender=random.choice(GENDER),
		# 		province='Maputo Province',
		# 		city='Maputo',
		# 		bairro=random.choice(BAIRROS),
		# 		quarteirao='A',
		# 		is_male=False
		# 	)
		# 	obj.save()
		# 	stud.parents.add(obj)
		# 	stud.save()
		# 	print(f'{stud} father generated successfully')



		# students = Student.objects.all()
		# for stud in students:
		# 	username = stud.first_name + stud.last_name
		# 	user = User.objects.create(
		# 		username=username)
		# 	user.save()

		# teachers = Teacher.objects.all()
		# for teacher in teachers:
		# 	username = teacher.first_name + teacher.last_name
		# 	user = User.objects.create(
		# 		username=username)
		# 	user.save()

		# subjects = SubjectName.objects.all()


		# turma = Turma.objects.get(name='B')
		# clss = Classe.objects.get(name='8ª classe', turma=turma)
		# students = Student.objects.filter(
		# 	classe=clss)
		# for student in students:
		# 	# print(json.dumps(student.serialize(), indent=4, default=str))
		# 	for subject_name in SUBJECT_NAMES:
		# 		for test_name in TEST_NAMES:
		# 			xmin = random.randint(1, 6)
		# 			xmax = random.randint(15, 20)
		# 			test_mark = random.randint(xmin, xmax)
		# 			subjects = student.subjects.all()
		# 			for subj in subjects:
		# 				s = SubjectName.objects.get(name=subject_name)
		# 				print(s)
		# 				if s == subj.subject:
		# 					test = Test.objects.create(
		# 						name=test_name,
		# 						mark=test_mark
		# 					)
		# 					test.save()
		# 					subj.tests.add(test)
		# 					print(f'Test {test_name!r} with mark {test_mark!r} added successfully for {student}')
							# print(json.dumps(student.serialize(), indent=4, default=str))			




		# student = Student.objects.get(
		# 	first_name='Michael', last_name='Smith')
		# print(json.dumps(student.serialize(), indent=4, default=str))
		# # print(dir(student.subjects))
		# test_name = 'Mathematics'
		# test_mark = 17.5
		# subjects = student.subjects.all()
		# for subj in subjects:
		# 	s = SubjectName.objects.get(name=test_name)
		# 	if s == subj.subject:
		# 		test = Test.objects.create(
		# 			name=test_name,
		# 			mark=test_mark
		# 		)
		# 		test.save()
		# 		subj.tests.add(test)
		# 		print(f'Test {test_name!r} with mark {test_mark!r} added successfully for {student}')
		# 		print(json.dumps(student.serialize(), indent=4, default=str))


		# decima_segunda = Classe.objects.get(name='12ª classe')
		# print(decima_segunda)
		# turma = Turma.objects.get(name='B')
		# decima_segunda = Classe.objects.create(
		# 	name='12ª classe',
		# 	turma=turma)
		# decima_segunda.save()

		# students = Student.objects.all()
		# for student in students:
		# 	parent = Parent.objects.create(
		# 		first_name=student.last_name,
		# 		last_name=faker.last_name_male(),
		# 		email=faker.email(),
		# 		phone_number=generate_phone_number(),
		# 		gender=random.choice(GENDER),
		# 		province='Maputo Province',
		# 		city='Maputo',
		# 		bairro=random.choice(BAIRROS),
		# 		quarteirao='A',
		# 		student=student
		# 	)
		# 	parent.save()
		# 	print(f'Parent {parent!r} created successfully')

		# students = Student.objects.all()
		# for stud in students:
			# stud.phone_number = generate_phone_number()
			# stud.email = stud.first_name.lower() + '.' + stud.last_name.lower() + '@educa.mz'
			# stud.save()



		# teachers = Teacher.objects.all()
		# for teacher in teachers:
		# 	teacher.phone_number = generate_phone_number()
		# 	teacher.email = teacher.first_name.lower() + '.' + teacher.last_name.lower() + '@educa.mz'
		# 	teacher.save()




		# turma = Turma.objects.get(name='B')
		# clss = Classe.objects.get(name='8ª classe', turma=turma)
		# subjects = SubjectName.objects.all()

		# for x in range(6):
		# 	teacher = Teacher.objects.create(
		# 		first_name=faker.first_name(),
		# 		last_name=faker.last_name(),
		# 		numero_de_bi=generate_IC(),
		# 		gender=random.choice(GENDER),
		# 		birth_date=faker.date_of_birth(),
		# 		province='Maputo Province',
		# 		city='Maputo',
		# 		bairro=random.choice(BAIRROS),
		# 		quarteirao='A'
		# 	)
		# 	print(f'{teacher} created successfully')
		# 	teacher.classe.add(clss)
			# stud.email = stud.first_name.lower() + '.' + stud.last_name.lower() + '@educa.mz'
			# teacher.save()
			# for sub in random.choices(subjects, k=random.randint(1, 3)):
			# 	teacher.subjects.add(sub)
			# 	teacher.save()
			# 	print(f'{sub.name!r} successfully registered for {teacher}')






		# turma = Turma.objects.get(name='B')
		# clss = Classe.objects.get(name='8ª classe', turma=turma)
		# subjects = SubjectName.objects.all()

		# for x in range(25):
		# 	stud = Student.objects.create(
		# 		first_name=faker.first_name(),
		# 		last_name=faker.last_name(),
		# 		numero_de_bi=generate_IC(),
		# 		phone_number=generate_phone_number(),
		# 		gender=random.choice(GENDER),
		# 		birth_date=faker.date_of_birth(),
		# 		province='Maputo Province',
		# 		city='Maputo',
		# 		bairro=random.choice(BAIRROS),
		# 		quarteirao='A',
		# 		father_name=faker.first_name_male() + ' ' + faker.last_name_male(),
		# 		mother_name=faker.first_name_female() + ' ' + faker.last_name_female(),
		# 		classe=clss
		# 	)
		# 	print(f'{stud} created successfully')
		# 	stud.save()
		# 	stud.email = stud.first_name.lower() + '.' + stud.last_name.lower() + '@educa.mz'
		# 	for sub in subjects:
		# 		su = SubjectMark.objects.create(
		# 			subject=sub)
		# 		su.save()
		# 		stud.subjects.add(su)
		# 		stud.save()
		# 		print(f'{su!r} successfully registered for {stud}')

		# students = Student.objects.filter(
		# 	classe=clss)
		# for student in students:
		# 	for subject_name in SUBJECT_NAMES:
		# 		for test_name in TEST_NAMES:
		# 			test_mark = random.randint(8, 20)
		# 			subjects = student.subjects.all()
		# 			for subj in subjects:
		# 				s = SubjectName.objects.get(name=subject_name)
		# 				print(s)
		# 				if s == subj.subject:
		# 					test = Test.objects.create(
		# 						name=test_name,
		# 						mark=test_mark
		# 					)
		# 					test.save()
		# 					subj.tests.add(test)
		# 					print(f'Test {test_name!r} with mark {test_mark!r} added successfully for {student}')





		# for x in range(8, 13):
		# 	name = f'{x}ª classe'
		# 	clss = Classe.objects.create(name=name)
		# 	clss.save()
		# 	print(f'Classe {clss.name!r} created successfully!')


		# for name in ['A', 'B', 'C']:
		# 	turma = Turma.objects.create(
		# 		name=name)
		# 	turma.save()
		# 	print(f'Turma {turma.name!r} created successfully!')

		# subjects = SubjectName.objects.all()
		# for sub in subjects:
		# 	su = SubjectMark.objects.create(
		# 		subject=sub)
		# 	su.save()
		# 	print(f'SubjectMark {su.subject.name!r} created successfully!')


		# for name in ['Mathematics', 'Physics', 'Chemistry', 'Biology', 'Portuguese',
		# 		  'Geography', 'English', 'History']:
		# 	subj = SubjectName.objects.create(
		# 		name=name)
		# 	subj.save()
		# 	print(f'{subj.name} created successfully!')

		self.stdout.write(self.style.SUCCESS('Successfully generated data.'))



