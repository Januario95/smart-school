from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

GENDER = (
	('male', 'Male'),
	('female', 'Female')
)
SEMESTERS = ((semester, semester) for semester in ('Primeiro', 'Segundo', 'Terceiro'))
DAYS = ((f'{x}ª Feira', f'{x}ª Feira') for x in range(2, 7))


# class SubjectClassHour(models.Model):
# 	subject = models.ForeignKey(
# 		to='SubjectNameNewModel', on_delete=models.CASCADE
# 	)
# 	class_time = models

# class TimetableDay(models.Model):
# 	day = models.CharField(
# 		choices=DAYS,
# 		default='2ª Feira'
# 	)
# 	subject_class_hour = models


class TeacherAndStudentMessage(models.Model):
	sender = models.ForeignKey(
		to='TeacherNameNewModel', on_delete=models.CASCADE
	)
	receiver = models.ForeignKey(
		to='StudentNameNewModel', on_delete=models.CASCADE
	)
	message = models.TextField()
	sent_at = models.DateTimeField(auto_now=True)
	resent_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f'Mensagens entre professor {self.sender.fullname()} e estudante {self.receiver.fullname}'
	
	class Meta:
		ordering = ('-sent_at',)
		verbose_name = 'Message (Teacher <> Student)'
		verbose_name_plural = 'Messages (Teacher <> Student)'

class SubjectTimetable(models.Model):
	subject_name = models.ForeignKey(
		to='SubjectNameNewModel', on_delete=models.CASCADE
	)
	class_day = models.CharField(
		max_length=10,
		choices=DAYS,
		default='2ª Feira'
	)
	class_start_time = models.TimeField()
	class_end_time = models.TimeField()

	def serialize(self):
		data = {
			'id': self.pk,
			'subject_name': self.subject_name.name,
			'class_day': self.class_day,
			'class_start_time': self.class_start_time,
			'class_end_time': self.class_end_time
		}
		return data

	def __str__(self):
		return f'{self.subject_name.name} - {self.class_day} - ({self.class_start_time} - {self.class_end_time})'
	
	class Meta:
		verbose_name = 'Subject Timetable'
		verbose_name_plural = 'Subject Timetable'

class TimeTable(models.Model):
	subjects =  models.ManyToManyField(
		to='SubjectTimeTable', blank=True)
	turma = models.ForeignKey(
		to='TurmaNewModel', on_delete=models.CASCADE
	)
	classe = models.ForeignKey(
		to='ClasseNewModel', on_delete=models.CASCADE
	)
	year = models.ForeignKey(to='Year', on_delete=models.CASCADE)
	semester = models.ForeignKey(
		to='SemesterNewModel', on_delete=models.CASCADE
	)

	def __str__(self):
		return f'Timetable for {self.classe} {self.turma}, {self.semester} Semestre of {self.year}'

class Attendance(models.Model):
	teacher = models.ForeignKey(to='TeacherNameNewModel', on_delete=models.CASCADE)
	student = models.ForeignKey(to='StudentNameNewModel', on_delete=models.CASCADE)
	subject = models.ForeignKey(to='SubjectNameNewModel', on_delete=models.CASCADE)
	semester = models.ForeignKey(to='SemesterModel', on_delete=models.CASCADE)
	reason = models.CharField(max_length=255, blank=True)
	is_present = models.BooleanField(default=False)
	class_time = models.DateTimeField() # auto_now=True)

	def __str__(self):
		presence = 'Is Present' if self.is_present else 'Not Present'
		return f'{self.student} - {presence}'
	
	def serialize(self):
		data = {
			'id': self.pk,
			'is_present': self.is_present,
			'class_time': self.class_time,
			'date': self.class_time.strftime('%d de %m de %Y'),
			'time': self.class_time.strftime('%H:%M:%S')
		}
		return data



class AdminToParentsMessage(models.Model):
	sender = models.ForeignKey(to=User, on_delete=models.CASCADE,
		blank=True)
	receiver = models.ForeignKey(to='ParentNameNewModel', on_delete=models.CASCADE,
		blank=True)
	message = models.CharField(max_length=255)
	sent_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return f'{self.sender} -> {self.receiver}'
	
	class Meta:
		ordering = ('sender',)
		verbose_name = 'Parent Admin Message'
		verbose_name_plural = 'Parent Admin Messages'


class ParentToAdminMessage(models.Model):
	sender = models.ForeignKey(to='ParentNameNewModel', on_delete=models.CASCADE,
		blank=True)
	receiver = models.ForeignKey(to=User, on_delete=models.CASCADE,
		blank=True)
	message = models.CharField(max_length=255)
	sent_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return f'{self.sender} -> {self.receiver}'
	
	class Meta:
		ordering = ('sender',)
		verbose_name = 'Admin Parent Message'
		verbose_name_plural = 'Admin Parent Messages'



class AdminToTeacherMessage(models.Model):
	sender = models.ForeignKey(to=User, on_delete=models.CASCADE,
		blank=True)
	receiver = models.ForeignKey(to='TeacherNameNewModel', on_delete=models.CASCADE,
		blank=True)
	message = models.CharField(max_length=255)
	sent_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return f'{self.sender} -> {self.receiver}'
	
	class Meta:
		ordering = ('sender',)
		verbose_name = 'Admin Teacher Message'
		verbose_name_plural = 'Admin Teacher Messages'


class StudentMessageAdmin(models.Model):
	sender = models.ForeignKey(to=User, on_delete=models.CASCADE,
		blank=True)
	receiver = models.ForeignKey(to='StudentNameNewModel', on_delete=models.CASCADE,
		blank=True)
	message = models.CharField(max_length=255)
	sent_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return f'{self.sender} -> {self.receiver}'
	
	class Meta:
		ordering = ('sender',)
		verbose_name = 'Admin Student Message'
		verbose_name_plural = 'Admin Student Messages'

class Year(models.Model):
	year = models.CharField(
		max_length=4, default=datetime.now().year,
		unique=True)

	def __str__(self):
		return self.year
	
class SemesterNewModel(models.Model):
    name = models.CharField(
        max_length=20, choices=SEMESTERS
    )
    year = models.CharField(max_length=4, default='2023')

    def __str__(self):
        return self.name
	
    def serialize(self):
        data = {
			'id': self.pk,
			'name': self.name,
			'year': self.year
        }
        return data
    
    class Meta:
        verbose_name = 'Semester Name'
        verbose_name_plural = 'Semester Names'
    
class ClasseNewModel(models.Model):
    CLASSES = ((f'{x}ª classe', f'{x}ª Classe') for x in range(7, 13))
    name = models.CharField(max_length=15, choices=CLASSES, unique=True)

    def __str__(self):
        return self.name
    
    def serialize(self):
        data = {
			'id': self.pk,
			'name': self.name
        }
        return data
    
    class Meta:
        ordering = ('id',)
        verbose_name = 'Classe'
        verbose_name_plural = 'Classes'
    
class TurmaNewModel(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name
    
    def serialize(self):
        data = {
			'id': self.pk,
			'name': self.name
        }
        return data
    
    class Meta:
        verbose_name = 'Turma'
        verbose_name_plural = 'Turmas'
	
class TestNewModel(models.Model):
    name = models.CharField(max_length=150)
    mark = models.DecimalField(decimal_places=1, max_digits=10)
    
    def __str__(self):
        return f'{self.name} - {self.mark}'
    
    def serialize(self):
        data = {
			'id': self.pk,
			'name': self.name,
			'mark': self.mark
        }
        return data

    class Meta:
        verbose_name = 'Test'
        verbose_name_plural = 'Tests'
	
class SubjectNameNewModel(models.Model):
	name = models.CharField(max_length=150)
	# class_is_active = models.BooleanField(default=False)

	def __str__(self):
		return self.name
    
	def serialize(self):
		data = {
			'id': self.pk,
			'name': self.name
        }
		return data
	
	class Meta:
		verbose_name = 'Subject Name'
		verbose_name_plural = 'Subjects Name'


class StudentAttendance(models.Model):
	student = models.ForeignKey(
		to='StudentNameNewModel', on_delete=models.CASCADE,
		null=True, blank=True
	)
	teacher = models.ForeignKey(
		to='TeacherNameNewModel', on_delete=models.CASCADE,
		null=True, blank=True
	)
	semester = models.ForeignKey(
		to=SemesterNewModel, on_delete=models.CASCADE,
		blank=True, null=True
	)
	classe = models.ForeignKey(
	    to=ClasseNewModel, on_delete=models.CASCADE,
		blank=True, null=True)
	year = models.ForeignKey(
	    to=Year, on_delete=models.CASCADE,
		blank=True, null=True
	)
	turma = models.ForeignKey(
	    to=TurmaNewModel, on_delete=models.CASCADE,
		blank=True, null=True)
	subject = models.ForeignKey(
		to=SubjectNameNewModel, on_delete=models.CASCADE,
		null=True, blank=True
	)
	class_datetime = models.DateTimeField(auto_now_add=True)
	attended = models.BooleanField(default=False)
	comment = models.TextField(blank=True, null=True)

	def serialize(self):
		data = {
			'pk': self.pk,
			'student': self.student,
			'teacher': self.teacher,
			'semester': self.semester.name,
			'subject': self.subject.name,
			'class_datetime': self.class_datetime,
			'attended': self.attended
		}
		return data

	def __str__(self):
		return f'{self.class_datetime}'
	
	class Meta:
		verbose_name = 'Student Attendance'
		verbose_name_plural = 'Student Attendances'


class SubjectTestsNewModel(models.Model):
    name = models.ForeignKey(to=SubjectNameNewModel, on_delete=models.CASCADE)
    link_is_open = models.BooleanField(default=False)
    tests = models.ManyToManyField(
	    to=TestNewModel, blank=True)
    attendance = models.ManyToManyField(
	    to=StudentAttendance, blank=True
	)
    
    def serialize(self):
        data = {
			'id': self.pk,
			'name': self.name,
			'tests': [test.serialize() for test in self.tests.all()]
        }
        return data
    
    def __str__(self):
	    return self.name.name

class SemesterModel(models.Model):
    USER_TYPES = (
	    ('teacher', 'teacher'),
	    ('student', 'student')
	)
    name = models.ForeignKey(
	    to=SemesterNewModel, on_delete=models.CASCADE)
    # name = models.CharField(
    #     max_length=20, choices=SEMESTERS,
    # )
    turma = models.ForeignKey(
	    to=TurmaNewModel, on_delete=models.CASCADE)
    classe = models.ForeignKey(
	    to=ClasseNewModel, on_delete=models.CASCADE)
    year = models.ForeignKey(
	    to=Year, on_delete=models.CASCADE, blank=True
	)
    user_type = models.CharField(
	    max_length=25,
	    choices=USER_TYPES,
	    default='student'
	)
    active_semester = models.BooleanField(default=False)
    subjects = models.ManyToManyField(
         to=SubjectTestsNewModel, blank=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    
    def get_nr_of_subjects(self):
        return self.subjects.count()

    def get_subjects_names(self):
        return [subj.name.name for subj in self.subjects.all()]
    
    def get_semester_final_avg(self):
        medias = self.get_semester_averages()
        totals = []
        for key, val in medias.items():
            totals.append(float(val))
        total = sum(totals) / len(totals)
        return str(round(total, 1)).replace(',', '.')

    def get_semester_averages(self):
        media_values = {}
        for subj in self.subjects.all():
            medias = []
            for test in subj.tests.all():
                medias.append(test.mark)

            media_final = round(sum(medias) / len(medias), 1)
            subject = subj.name.name

            row = {f'avg_{subject.lower()}': str(media_final).replace(',', '.')}
            media_values.update(row)
        return media_values

    def serialize(self):
        data = {
			'id': self.pk,
			'name': self.name.serialize(),
			'turma,': self.turma.serialize(),
			'classe': self.classe.serialize(),
			'year': self.year,
			# 'semester': self.semester.serialize(),
			'subjects': [subject.serialize() for subject in self.subjects.all()]
        }
        return data
    
    class Meta:
        verbose_name = 'Semester'
        verbose_name_plural = 'Semester'
    
    def __str__(self):
	    return self.name.name

class SubjectNewModel(models.Model):
    name = models.ForeignKey(to=SubjectNameNewModel, on_delete=models.CASCADE)
    tests = models.ManyToManyField(
	    to=TestNewModel, blank=True)
    turma = models.ForeignKey(
	    to=TurmaNewModel, on_delete=models.CASCADE, blank=True)
    classe = models.ForeignKey(
	    to=ClasseNewModel, on_delete=models.CASCADE, blank=True)
    semester = models.ForeignKey(
	    to=SemesterNewModel, on_delete=models.CASCADE, blank=True)

    def __str__(self):
        return f'{self.name}'
    
    def serialize(self):
        data = {
			'id': self.pk,
			'name': self.name.serialize(),
			'turma,': self.turma.serialize(),
			'classe': self.classe.serialize(),
			'semester': self.semester.serialize(),
			'tests': [test.serialize() for test in self.tests.serialize()]
        }
        return data
    
    class Meta:
        verbose_name = 'Subject'
        verbose_name_plural = 'Subjects'

class StudentNameNewModel(models.Model):
    user = models.ForeignKey(
	    to=User, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    numero_de_bi = models.CharField(max_length=13,
		blank=True)
    gender = models.CharField(
		max_length=6,
		choices=GENDER,
		default='male')
    birth_date = models.DateField()
    phone_number = models.CharField(
	    max_length=13, blank=True,
		null=True)
    email = models.EmailField(blank=True, null=True)
    profile_pic = models.ImageField(upload_to='profiles/%Y/%m/%d', default='/media/profile_image2_removebg.png')
    province = models.CharField(max_length=30)
    city = models.CharField(max_length=50)
    bairro = models.CharField(max_length=50,
			      blank=True)
    quarteirao = models.CharField(max_length=50,
			      blank=True)
    parents = models.ManyToManyField(
	    to='ParentNameNewModel', blank=True
	)
    subjects = models.ManyToManyField(
	    to=SubjectNewModel, blank=True
	)
    new_semester = models.ManyToManyField(
	    to=SemesterModel, blank=True
	)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    
    year = models.ManyToManyField(
	    to=Year,
		blank=True
	)
    # semester = models.ForeignKey(
	#     to=SemesterNewModel, on_delete=models.CASCADE, blank=True, null=True)
    # classe = models.ForeignKey(
	#     to=ClasseNewModel, on_delete=models.CASCADE, blank=True, null=True)
    # turma = models.ForeignKey(
	#     to=TurmaNewModel, on_delete=models.CASCADE, blank=True, null=True)
    
	
    def fullname(self):
        return f'{self.first_name} {self.last_name}'
	
    def serialize(self):
        data = {
			'id': self.pk,
			'first_name': self.first_name,
			'last_name': self.last_name,
			'phone_number': self.phone_number,
			'email': self.email,
			'numero_de_bi': self.numero_de_bi,
			'gender': self.gender,
			'birth_date': self.birth_date,
			'phone_number': self.phone_number,
			'province': self.province,
			'city': self.city,
			'bairro': self.bairro,
			'quarteirao': self.quarteirao,
			'parents': [parent.serialize() for parent in self.parents.all()]
        }
        return data

    def serialize_basic_info(self):
        data = {
			'id': self.pk,
			'first_name': self.first_name,
			'last_name': self.last_name,
			'phone_number': self.phone_number,
			'email': self.email
        }
        return data
    
    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Student'
        verbose_name_plural = 'Students'
    
    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name}'
    

class ParentNameNewModel(models.Model):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    numero_de_bi = models.CharField(max_length=13,
		blank=True)
    gender = models.CharField(
		max_length=6,
		choices=GENDER,
		default='male')
    phone_number = models.CharField(
	    max_length=13, blank=True,
		null=True)
    job_title = models.CharField(
		max_length=100,
		blank=True)
    email = models.EmailField(blank=True, null=True)
    province = models.CharField(max_length=30)
    city = models.CharField(max_length=50)
    bairro = models.CharField(max_length=50,
			      blank=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    
    def serialize(self):
        data = {
			'id': self.pk,
			'first_name': self.first_name,
			'last_name': self.last_name,
			'gender': self.gender,
			'phone_number': self.phone_number,
			'email': self.email,
			'province': self.province,
			'city': self.city,
			'bairro': self.bairro
        }
        return data
    
    def is_male(self):
        return self.gender == 'male'
    
    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Parent'
        verbose_name_plural = 'Parents'
    
    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name}'
    

class TeacherClassAttendance(models.Model):
	teacher = models.ForeignKey(
		to='TeacherNameNewModel', on_delete=models.CASCADE
	)
	turma = models.ForeignKey(
	    to=TurmaNewModel, on_delete=models.CASCADE, null=True, blank=True)
	classe = models.ForeignKey(
	    to=ClasseNewModel, on_delete=models.CASCADE, null=True, blank=True)
	subject = models.ForeignKey(
		to=SubjectNameNewModel, on_delete=models.CASCADE, null=True, blank=True
	)
	class_date = models.DateField()
	class_time = models.TimeField()
	attended = models.BooleanField(default=False)

	def __str__(self):
		return f'{self.teacher} - {self.class_date} - {self.class_time}'


class TeacherSchoolAttended(models.Model):
	DEGREES = (
		('Nivel Medio', 'Nivel Medio'),
		('Licenciatura', 'Licenciatura'),
		('Mestrado', 'Mestrado'),
		('Doutoramento', 'Doutoramento')
	)
	name = models.CharField(max_length=255)
	degree = models.CharField(
		max_length=50,
		choices=DEGREES,
		default='Licenciatura'
	)
	major = models.CharField(max_length=255)
	city = models.CharField(max_length=100)
	country = models.CharField(max_length=50)
	start_date = models.DateField()
	end_date = models.DateField()

	def __str__(self):
		return f'{self.name}'
	
	def serialize(self):
		data = {
			'id': self.pk,
			'name': self.name,
			'degree': self.degree,
			'major': self.major,
			'city': self.city,
			'country': self.country,
			'start_date': self.start_date,
			'end_date': self.end_date
		}
		return data
	

class AttendanceURL(models.Model):
	url = models.URLField()
	open_time = models.DateTimeField()
	close_time = models.DateTimeField()

	def __str__(self):
		return f'{self.url} - [{self.open_time} - {self.close_time}]'
	
class AttendanceQRcode(models.Model):
	image = models.ImageField(upload_to='media/')

	def __str__(self):
		return f'{self.image.url}'

class TeacherNameNewModel(models.Model):
    user = models.ForeignKey(
	    to=User, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    numero_de_bi = models.CharField(max_length=13,
		blank=True)
    gender = models.CharField(
		max_length=6,
		choices=GENDER,
		default='male')
    birth_date = models.DateField()
    phone_number = models.CharField(
	    max_length=13, blank=True,
		null=True)
    email = models.EmailField(blank=True, null=True)
    profile_pic = models.ImageField(upload_to='profiles/%Y/%m/%d', default='/media/profile_image2_removebg.png')
    province = models.CharField(max_length=30)
    city = models.CharField(max_length=50)
    bairro = models.CharField(max_length=50,
			      blank=True)
    quarteirao = models.CharField(max_length=50,
			      blank=True)
    school_attended = models.ManyToManyField(
	    to=TeacherSchoolAttended, blank=True
	)
    subjects = models.ManyToManyField(
	    to=SubjectNewModel, blank=True
	)
    new_semester = models.ManyToManyField(
	    to=SemesterModel, blank=True
	)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    # class_attendance = models.ManyToManyField(
	#     to=TeacherClassAttendance, blank=True
	# )
    
    def serialize(self):
        data = {
			'id': self.pk,
			'first_name': self.first_name,
			'last_name': self.last_name,
			'semesters': [semester.serialize() for semester in self.new_semester.all()],
        }
        return data
    
    def serialize_basic_info(self):
        data = {
			'id': self.pk,
			'first_name': self.first_name,
			'last_name': self.last_name,
			'phone_number': self.phone_number,
			'email': self.email,
			'gender': self.gender,
			'phone_number': self.phone_number,
			'province': self.province,
			'city': self.city,
			'bairro': self.bairro,
			'quarteirao': self.quarteirao,
        }
        return data
    
    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Teacher New'
        verbose_name_plural = 'Teachers New'
    
    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name}'
    
    def fullname(self):
	    return f'{self.first_name} {self.last_name}'
    













	



























