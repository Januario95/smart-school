from django.shortcuts import render, redirect
from django.contrib.auth.decorators import (
	login_required
)
from django.shortcuts import (
    render, redirect, get_object_or_404
)
from django.db.models import Q
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.views.decorators.cache import cache_page
from django.contrib.auth import (
	authenticate, login as auth_login, logout
)

from app2.models import (
    SemesterNewModel, ClasseNewModel, TurmaNewModel, 
	StudentNameNewModel, SubjectNewModel,
    SubjectTestsNewModel,
    SubjectNameNewModel, Year, SemesterModel, TeacherNameNewModel,
    StudentMessageAdmin, ParentToAdminMessage, AdminToParentsMessage, 
	AdminToTeacherMessage, Attendance, ParentNameNewModel,
	TimeTable, SubjectTimetable, TeacherClassAttendance,
	TeacherClassAttendance, StudentAttendance,
)
from app2.forms import (
    UpdateStudentForm, YearSemesterClasseTurmForm,
    YearSemesterClasseTurmSubjectForm,
)
from .views_teacher import (
    check_semesters_are_equal, formart_date, format_gender
)

import json



@login_required
def student_profile(request, student_pk):
    if request.user.is_superuser:
        message = 'Acesso negado. Nao tem permissao para ver essa pagina.'
        return render(request,
					  'pages/auth/unauthorized.html',
					  {'message': message})
    
    if not request.user.is_staff:
        student = StudentNameNewModel.objects.filter(pk=student_pk)
        if student.exists():
            student = student.first()
            user = request.user
            # print(user, student.user, user == student.user)
            if user == student.user:
                return render(request,
                                'pages/students/student_profile.html',
                                {'student': student})
            else:
                message = 'Acesso negado. Nao tem permissao para ver essa pagina.'
                return render(request,
                            'pages/auth/unauthorized.html',
                            {'message': message})
        else:
            message = 'Acesso negado. Nao tem permissao para ver essa pagina.'
            return render(request,
                        'pages/auth/unauthorized.html',
                        {'message': message})
    else:
        message = 'Acesso negado. Nao tem permissao para ver essa pagina.'
        return render(request,
					  'pages/auth/unauthorized.html',
					  {'message': message})


@login_required
def student_update_profile(request, student_pk):
    print('Homepage')
    print(request.user.is_staff == False)
    if request.user.is_superuser:
        message = 'Acesso negado. Nao tem permissao para ver essa pagina.'
        return render(request,
					  'pages/auth/unauthorized.html',
					  {'message': message})
    
    if not request.user.is_staff:
        student = StudentNameNewModel.objects.filter(pk=student_pk)
        print(student.exists())
        if student.exists():
            student = student.first()
            user = request.user
            if user == student.user:
                initial = {
                    'first_name': student.first_name, 'last_name': student.last_name,
                    'email': student.email, 'ic_number': student.numero_de_bi,
                    'gender': format_gender(student.gender).lower(), 'birth_date': formart_date(student.birth_date),
                    'phone_number': student.phone_number, 'province': student.province,
                    'city': student.city, 'bairro': student.bairro, 'quarteirao': student.quarteirao,
                }
                if request.method == 'POST':
                    form = UpdateStudentForm(request.POST, request.FILES)
                    if form.is_valid():
                        inner_data = form.cleaned_data
                        print(inner_data)
                        student.email = inner_data.get('email')
                        student.first_name = inner_data.get('first_name')
                        student.last_name = inner_data.get('last_name')
                        student.numero_de_bi = inner_data.get('ic_number')
                        student.gender = inner_data.get('gender')
                        student.birth_date = inner_data.get('birth_date')
                        student.phone_number = inner_data.get('phone_number')
                        student.province = inner_data.get('province')
                        student.city = inner_data.get('city')
                        student.bairro = inner_data.get('bairro')
                        gender = inner_data.get('gender')
                        print(gender)
                        if gender == 'feminino':
                            student.gender = 'female'
                        if gender == 'masculino':
                            student.gender = 'male'

                        student.quarteirao = inner_data.get('quarteirao')
                        profile_pic = inner_data.get('profile_pic')
                        if profile_pic:
                            student.profile_pic = profile_pic
                        student.save()

                        initial = {
							'first_name': student.first_name, 'last_name': student.last_name,
							'email': student.email, 'ic_number': student.numero_de_bi,
							'gender': format_gender(student.gender).lower(), 
                            'birth_date': formart_date(student.birth_date),
							'phone_number': student.phone_number, 'province': student.province,
							'city': student.city, 'bairro': student.bairro, 
                            'quarteirao': student.quarteirao,
                        }
                        form = UpdateStudentForm(initial=initial)
                    else:
                        print(form.errors)
                else:
                    form = UpdateStudentForm(initial=initial)
                    
                return render(request,
                                'pages/students/student_update_profile.html',
                                {'student': student, 'form': form})
            else:
                message = 'Acesso negado. Nao tem permissao para ver essa pagina.'
                return render(request,
                            'pages/auth/unauthorized.html',
                            {'message': message})
        else:
            message = 'Acesso negado. Nao tem permissao para ver essa pagina.'
            return render(request,
                        'pages/auth/unauthorized.html',
                        {'message': message})
    else:
        message = 'Acesso negado. Nao tem permissao para ver essa pagina.'
        return render(request,
					  'pages/auth/unauthorized.html',
					  {'message': message})

@login_required
def student_profile_teacher_info(request, teacher_pk, student_pk, year_name, 
                                 semester_name, classe_name, turma_name):
    student_current_sem_subjects = []
    teacher_unique_subjects = []
    try:
        teacher = TeacherNameNewModel.objects.get(pk=teacher_pk)
        # print(teacher)
        student = StudentNameNewModel.objects.get(pk=student_pk)
        # print(student)
        year = Year.objects.get(year=year_name)
        semester_name = SemesterNewModel.objects.get(name=semester_name)
        classe = ClasseNewModel.objects.get(name=classe_name)
        turma = TurmaNewModel.objects.get(name=turma_name)
        new_semester = SemesterModel.objects.filter(
            year=year,
            name=semester_name,
            classe=classe,
            turma=turma
        )
        # print(new_semester)
        if new_semester.exists():
            new_semester = new_semester.first()
            
            teacher_semesters = teacher.new_semester.all()
            # print(teacher_semesters)
            for teacher_sem in teacher_semesters:
                # print(f'({teacher_sem.year}, {new_semester.year}), ({teacher_sem.name}, {new_semester.name}), ({teacher_sem.classe}, {new_semester.classe}), ({teacher_sem.turma}, {new_semester.turma})')
                if check_semesters_are_equal(teacher_sem, new_semester):
                    subjects = teacher_sem.subjects.all()
                    print(subjects)
                    for subj in subjects:
                        if subj not in teacher_unique_subjects:
                            teacher_unique_subjects.append(subj.name.name)
            # print(teacher_unique_subjects)

            student_semesters = student.new_semester.all()
            for stud_sem in student_semesters:
                if check_semesters_are_equal(stud_sem, new_semester):
                    subjects = stud_sem.subjects.all()
                    # print(subjects)
                    for subj in subjects:
                        if subj.name in teacher_unique_subjects:
                            student_current_sem_subjects.append(subj.name.serialize())
            # print(student_current_sem_subjects)
            student = student.serialize()
    except Exception as e:
        print(e.args)
        teacher = None
        student = None

    # print(student_current_sem_subjects)

    if teacher:
        teacher = teacher.serialize_basic_info()

    return JsonResponse({
        'teacher': teacher,
        'teacher_unique_subjects': teacher_unique_subjects
    })


@login_required
def student_teachers(request, student_pk):
    if request.user.is_superuser:
        message = 'Acesso negado. Nao tem permissao para ver essa pagina.'
        return render(request,
					  'pages/auth/unauthorized.html',
					  {'message': message})
    
    if not request.user.is_staff:
        student = StudentNameNewModel.objects.filter(pk=student_pk)
        if student.exists():
            student = student.first()
            user = request.user
            # print(user, student.user, user == student.user)
            if user == student.user:
                current_semester = []
                teachers = []
                teacher_data = []
                year_name = None
                semester_name = None
                turma_name = None
                classe_name = None
                if request.method == 'POST':
                    form = YearSemesterClasseTurmForm(request.POST)
                    if form.is_valid():
                        inner_data = form.cleaned_data
                        # print(inner_data)
                        year_name = inner_data.get('year')
                        year = Year.objects.get(year=year_name)
                        semester_name = inner_data.get('semester')
                        turma_name = inner_data.get('turma')
                        turma = TurmaNewModel.objects.get(name=turma_name)
                        classe_name = inner_data.get('classe')
                        classe = ClasseNewModel.objects.get(name=classe_name)
                        semester = SemesterNewModel.objects.get(name=semester_name)
                        new_semester = SemesterModel.objects.filter(
                            name=semester,
                            year=year,
                            classe=classe,
                            turma=turma
                        )
                        # print(new_semester)
                        teachers = TeacherNameNewModel.objects.filter(
                             new_semester__in=new_semester
						)
                        # print(teachers)
                        
                        if new_semester.exists():
                            new_semester = new_semester.first()
                            for teacher in teachers:
                                teacher_info = teacher.serialize_basic_info()
                                teacher_semesters = teacher.new_semester.all()
                                for teacher_sem in teacher_semesters:
                                     if check_semesters_are_equal(teacher_sem, new_semester):
                                          subjects = teacher_sem.subjects.all()
                                          print(subjects)
                                          teacher_info['subjects'] = [subj.name.name for subj in subjects]
                                print(teacher_info) 
                                teacher_data.append(teacher_info)
                    else:
                        print(form.errors)
                else:
                    form = YearSemesterClasseTurmForm()
                    
                return render(request,
                                'pages/students/student_teachers.html',
                                {'student': student, 'form': form, 'current_semester': current_semester,
                                 'teachers': teachers, 'year_name': year_name, 'turma_name': turma_name,
                                 'semester_name': semester_name, 'classe_name': classe_name,
                                 'teacher_data': teacher_data})
            else:
                message = 'Acesso negado. Nao tem permissao para ver essa pagina.'
                return render(request,
                            'pages/auth/unauthorized.html',
                            {'message': message})
        else:
            message = 'Acesso negado. Nao tem permissao para ver essa pagina.'
            return render(request,
                        'pages/auth/unauthorized.html',
                        {'message': message})
    else:
        message = 'Acesso negado. Nao tem permissao para ver essa pagina.'
        return render(request,
					  'pages/auth/unauthorized.html',
					  {'message': message})
    

@login_required
def student_view_attendance(request, student_pk):
    if request.user.is_superuser:
        message = 'Acesso negado. Nao tem permissao para ver essa pagina.'
        return render(request,
					  'pages/auth/unauthorized.html',
					  {'message': message})
    
    if not request.user.is_staff:
        student = StudentNameNewModel.objects.filter(pk=student_pk)
        if student.exists():
            student = student.first()
            user = request.user
            # print(user, student.user, user == student.user)
            if user == student.user:
                current_semester = []
                teachers = []
                teacher_data = []
                year_name = None
                semester_name = None
                turma_name = None
                classe_name = None
                atttendances = []
                if request.method == 'POST':
                    form = YearSemesterClasseTurmForm(request.POST)
                    if form.is_valid():
                        inner_data = form.cleaned_data
                        # print(inner_data)
                        year_name = inner_data.get('year')
                        year = Year.objects.get(year=year_name)
                        semester_name = inner_data.get('semester')
                        turma_name = inner_data.get('turma')
                        turma = TurmaNewModel.objects.get(name=turma_name)
                        classe_name = inner_data.get('classe')
                        classe = ClasseNewModel.objects.get(name=classe_name)
                        semester = SemesterNewModel.objects.get(name=semester_name)
                        new_semester = SemesterModel.objects.filter(
                            name=semester,
                            year=year,
                            classe=classe,
                            turma=turma
                        )
                        print(new_semester)
                        if new_semester.exists():
                            new_semester = new_semester.first()

                            atttendances = StudentAttendance.objects.filter(
                                student=student,
                                semester=new_semester.name,
                                classe=classe,
                                turma=turma
                            )
                            print(atttendances)
                    else:
                        print(form.errors)
                else:
                    form = YearSemesterClasseTurmForm()
                    
                return render(request,
                                'pages/students/student_view_attendance.html',
                                {'student': student, 'form': form, 'atttendances': atttendances,
                                 'year_name': year_name, 'turma_name': turma_name,
                                 'semester_name': semester_name, 'classe_name': classe_name,
                                 'teacher_data': teacher_data})
            else:
                message = 'Acesso negado. Nao tem permissao para ver essa pagina.'
                return render(request,
                            'pages/auth/unauthorized.html',
                            {'message': message})
        else:
            message = 'Acesso negado. Nao tem permissao para ver essa pagina.'
            return render(request,
                        'pages/auth/unauthorized.html',
                        {'message': message})
    else:
        message = 'Acesso negado. Nao tem permissao para ver essa pagina.'
        return render(request,
					  'pages/auth/unauthorized.html',
					  {'message': message})


@login_required
def student_view_attendance_by_subject(request, student_pk):
    if request.user.is_superuser:
        message = 'Acesso negado. Nao tem permissao para ver essa pagina.'
        return render(request,
					  'pages/auth/unauthorized.html',
					  {'message': message})
    
    if not request.user.is_staff:
        student = StudentNameNewModel.objects.filter(pk=student_pk)
        if student.exists():
            student = student.first()
            user = request.user
            # print(user, student.user, user == student.user)
            if user == student.user:
                current_semester = []
                teachers = []
                teacher_data = []
                year_name = None
                semester_name = None
                turma_name = None
                classe_name = None
                subject_name = None
                atttendances = []
                if request.method == 'POST':
                    form = YearSemesterClasseTurmSubjectForm(request.POST)
                    if form.is_valid():
                        inner_data = form.cleaned_data
                        # print(inner_data)
                        year_name = inner_data.get('year')
                        year = Year.objects.get(year=year_name)
                        semester_name = inner_data.get('semester')
                        turma_name = inner_data.get('turma')
                        turma = TurmaNewModel.objects.get(name=turma_name)
                        classe_name = inner_data.get('classe')
                        classe = ClasseNewModel.objects.get(name=classe_name)
                        semester = SemesterNewModel.objects.get(name=semester_name)
                        subject_name = inner_data.get('subject')
                        subject = SubjectNameNewModel.objects.filter(name=subject_name)
                        if subject.exists():
                            subject = subject.first()

                            new_semester = SemesterModel.objects.filter(
                                name=semester,
                                year=year,
                                classe=classe,
                                turma=turma
                            )
                            print(new_semester)
                            if new_semester.exists():
                                new_semester = new_semester.first()

                                atttendances = StudentAttendance.objects.filter(
                                    student=student,
                                    semester=new_semester.name,
                                    classe=classe,
                                    turma=turma,
                                    subject=subject
                                )
                                print(atttendances)
                    else:
                        print(form.errors)
                else:
                    form = YearSemesterClasseTurmSubjectForm()
                    
                return render(request,
                                'pages/students/student_view_attendance_by_subject.html',
                                {'student': student, 'form': form, 'atttendances': atttendances,
                                 'year_name': year_name, 'turma_name': turma_name,
                                 'semester_name': semester_name, 'classe_name': classe_name,
                                 'subject_name': subject_name, 'teacher_data': teacher_data})
            else:
                message = 'Acesso negado. Nao tem permissao para ver essa pagina.'
                return render(request,
                            'pages/auth/unauthorized.html',
                            {'message': message})
        else:
            message = 'Acesso negado. Nao tem permissao para ver essa pagina.'
            return render(request,
                        'pages/auth/unauthorized.html',
                        {'message': message})
    else:
        message = 'Acesso negado. Nao tem permissao para ver essa pagina.'
        return render(request,
					  'pages/auth/unauthorized.html',
					  {'message': message})


