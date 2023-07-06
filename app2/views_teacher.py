from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.views.decorators.http import require_POST
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
import os
import segno
import urllib.parse
import pandas as pd
from segno import helpers

from app2.models import (
    SemesterNewModel, ClasseNewModel, TurmaNewModel, 
	StudentNameNewModel, SubjectNewModel,
    SubjectTestsNewModel,
    SubjectNameNewModel, Year, SemesterModel, TeacherNameNewModel,
    StudentMessageAdmin, ParentToAdminMessage, AdminToParentsMessage, 
	AdminToTeacherMessage, Attendance, ParentNameNewModel,
	TimeTable, SubjectTimetable, TeacherClassAttendance,
	TeacherClassAttendance, StudentAttendance, AttendanceQRcode,
    TestNewModel,
)
from .forms import (
    TimeTableForm, StudentAttendanceForm, AddStudentMarkForm,
    AddStudentMarkFromFileForm, StudentMarkForm, StudentAllMarkForm,
    UpdateTeacherForm, StudentStatisticsForms, YearSemesterClasseTurmForm,
    YearSemesterForm, AttentanceForm,
)

import json
from datetime import datetime

def check_semesters_are_equal(sem1, sem2):
    return (sem1.year == sem2.year and
            sem1.name == sem2.name and
            sem1.classe == sem2.classe and
            sem1.turma == sem2.turma)

@login_required
def teacher_profile(request, teacher_pk):
    if request.user.is_superuser:
        message = 'Acesso negado. Nao tem permissao para ver essa pagina.'
        return render(request,
					  'pages/auth/unauthorized.html',
					  {'message': message})
    
    if request.user.is_staff:
        teacher = TeacherNameNewModel.objects.filter(pk=teacher_pk)
        if teacher.exists():
            teacher = teacher.first()
            user = request.user
            print(user)
            if user == teacher.user:
                return render(request,
                                'pages/teacher/teacher_profile.html',
                                {'teacher': teacher})
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
def teacher_students_info(request, teacher_pk):
    if request.user.is_superuser:
        message = 'Acesso negado. Nao tem permissao para ver essa pagina.'
        return render(request,
					  'pages/auth/unauthorized.html',
					  {'message': message})
    
    if request.user.is_staff:
        teacher = TeacherNameNewModel.objects.filter(pk=teacher_pk)
        if teacher.exists():
            teacher = teacher.first()
            user = request.user
            if user == teacher.user:
                subjects = []
                students = []
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
                        students = StudentNameNewModel.objects.filter(
                            new_semester__in=new_semester
                        )
                        # print(students)
                        if new_semester.exists():
                            new_semester = new_semester.first()
                            teacher_semesters = teacher.new_semester.all()
                            for teacher_sem in teacher_semesters:
                                if check_semesters_are_equal(teacher_sem, new_semester):
                                    # print(teacher_sem)
                                    subjects = teacher_sem.subjects.all()
                                    
                    else:
                        print(form.errors)
                else:
                    form = YearSemesterClasseTurmForm()

                return render(request,
                                'pages/teacher/teacher_students_info.html',
                                {'teacher': teacher, 'form': form, 'subjects': subjects,
                                 'students': students, 'year_name': year_name, 
                                 'semester_name': semester_name, 'classe_name': classe_name, 
                                 'turma_name': turma_name})
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
def teacher_profile_student_info(request, teacher_pk, student_pk, year_name, 
                                 semester_name, classe_name, turma_name):
    student_current_sem_subjects = []
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
            teacher_unique_subjects = []
            for teacher_sem in teacher_semesters:
                if check_semesters_are_equal(teacher_sem, new_semester):
                    subjects = teacher_sem.subjects.all()
                    for subj in subjects:
                        if subj not in teacher_unique_subjects:
                            teacher_unique_subjects.append(subj.name)
            # print(teacher_unique_subjects)

            student_semesters = student.new_semester.all()
            for stud_sem in student_semesters:
                if check_semesters_are_equal(stud_sem, new_semester):
                    subjects = stud_sem.subjects.all()
                    # print(subjects)
                    for subj in subjects:
                        if subj.name in teacher_unique_subjects:
                            student_current_sem_subjects.append(subj.name.serialize())
            print(student_current_sem_subjects)
            student = student.serialize()
    except Exception as e:
        print(e.args)
        teacher = None
        student = None

    # print(student_current_sem_subjects)

    if teacher:
        teacher = teacher.serialize_basic_info()

    return JsonResponse({
        'student': student,
        'student_current_sem_subjects': student_current_sem_subjects
    })


@login_required
def teacher_profile_school_info(request, teacher_pk):
    if request.user.is_superuser:
        message = 'Acesso negado. Nao tem permissao para ver essa pagina.'
        return render(request,
					  'pages/auth/unauthorized.html',
					  {'message': message})
    
    if request.user.is_staff:
        teacher = TeacherNameNewModel.objects.filter(pk=teacher_pk)
        if teacher.exists():
            teacher = teacher.first()
            user = request.user
            if user == teacher.user:
                students = []
                year_name = None
                semester_name = None
                turma_name = None
                classe_name = None
                unique_semesters = []
                semesters = []
                if request.method == 'POST':
                    form = YearSemesterForm(request.POST)
                    if form.is_valid():
                        inner_data = form.cleaned_data
                        # print(inner_data)
                        year = inner_data.get('year')
                        year_name = year
                        year = Year.objects.get(year=year)
                        # classe = inner_data.get('classe')
                        # classe_name = classe
                        # classe = ClasseNewModel.objects.get(name=classe)
                        semester = inner_data.get('semester')
                        semester_name = semester
                        # print(semester_name)
                        semester = SemesterNewModel.objects.get(name=semester)
                        new_semester = SemesterModel.objects.filter(
                            name=semester,
                            year=year
                        )
                        print(new_semester)
                        semesters = SemesterNewModel.objects.all()
                        if new_semester.exists():
                            new_semester = new_semester.first()
                            teacher_semesters = teacher.new_semester.all()
                            
                            for sem in teacher_semesters:
                                if (sem.year == new_semester.year and
                                    sem.name == new_semester.name):
                                    print(sem)
                                    unique_semesters.append(sem)
                            print(unique_semesters)
                    else:
                        print(form.errors)
                else:
                    form = YearSemesterForm()

                return render(request,
                                'pages/teacher/teacher_profile_school_info.html',
                                {'teacher': teacher, 'form': form, 'year_name': year_name,
                                 'unique_semesters': unique_semesters, 'semesters': semesters,
                                 'semester_name': semester_name, 'classe_name': classe_name,
                                 'turma_name': turma_name})
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
def teacher_profile_personal_info(request, teacher_pk):
    if request.user.is_superuser:
        message = 'Acesso negado. Nao tem permissao para ver essa pagina.'
        return render(request,
					  'pages/auth/unauthorized.html',
					  {'message': message})
    
    if request.user.is_staff:
        teacher = TeacherNameNewModel.objects.filter(pk=teacher_pk)
        if teacher.exists():
            teacher = teacher.first()
            user = request.user
            if user == teacher.user:
                return render(request,
                                'pages/teacher/teacher_profile_personal_info.html',
                                {'teacher': teacher})
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
    

def formart_date(date):
    date = date.strftime('%Y-%m-%d')
    return date

def format_gender(value):
	if value == 'female':
		return 'Feminino'
	if value == 'male':
		return 'Masculino'

@login_required
def teacher_profile_update_acc_info(request, teacher_pk):
    if request.user.is_superuser:
        message = 'Acesso negado. Nao tem permissao para ver essa pagina.'
        return render(request,
					  'pages/auth/unauthorized.html',
					  {'message': message})
    
    if request.user.is_staff:
        teacher = TeacherNameNewModel.objects.filter(pk=teacher_pk)
        if teacher.exists():
            teacher = teacher.first()
            user = request.user
            if user == teacher.user:
                initial = {
                    'first_name': teacher.first_name, 'last_name': teacher.last_name,
                    'email': teacher.email, 'ic_number': teacher.numero_de_bi,
                    'gender': format_gender(teacher.gender).lower(), 'birth_date': formart_date(teacher.birth_date),
                    'phone_number': teacher.phone_number, 'province': teacher.province,
                    'city': teacher.city, 'bairro': teacher.bairro, 'quarteirao': teacher.quarteirao,
                }
                print(format_gender(teacher.gender).lower())
                if request.method == 'POST':
                    form = UpdateTeacherForm(request.POST, request.FILES)
                    if form.is_valid():
                        inner_data = form.cleaned_data
                        # print(inner_data)
                        teacher.email = inner_data.get('email')
                        teacher.first_name = inner_data.get('first_name')
                        teacher.last_name = inner_data.get('last_name')
                        teacher.numero_de_bi = inner_data.get('ic_number')
                        teacher.gender = inner_data.get('gender')
                        teacher.birth_date = inner_data.get('birth_date')
                        teacher.phone_number = inner_data.get('phone_number')
                        teacher.province = inner_data.get('province')
                        teacher.city = inner_data.get('city')
                        teacher.bairro = inner_data.get('bairro')
                        gender = inner_data.get('gender')
                        print(gender)
                        if gender == 'feminino':
                            teacher.gender = 'female'
                        if gender == 'masculino':
                            teacher.gender = 'male'
                        # teacher.bairro = genero
                        teacher.quarteirao = inner_data.get('quarteirao')
                        profile_pic = inner_data.get('profile_pic')
                        if profile_pic:
                            teacher.profile_pic = profile_pic
                        teacher.save()
            
                        initial = {
                            'first_name': teacher.first_name, 'last_name': teacher.last_name,
                            'email': teacher.email, 'ic_number': teacher.numero_de_bi,
                            'gender': format_gender(teacher.gender).lower(), 'birth_date': formart_date(teacher.birth_date),
                            'phone_number': teacher.phone_number, 'province': teacher.province,
                            'city': teacher.city, 'bairro': teacher.bairro, 'quarteirao': teacher.quarteirao,
                        }

                        university = inner_data.get('university')
                        degree = inner_data.get('degree')
                        curso = inner_data.get('curso')
                        country_of_study = inner_data.get('country_of_study')
                        city_of_study = inner_data.get('city_of_study')
                        study_start_date = inner_data.get('study_start_date')
                        study_end_date = inner_data.get('study_end_date')

                        school_attended = teacher.school_attended.all()
                        for school in school_attended:
                            # print(json.dumps(school.serialize(), indent=4, default=str))
                            try:
                                school.name = university
                                school.degree = degree
                                school.major = curso
                                school.country = country_of_study
                                school.city = city_of_study
                                school.start_date = study_start_date
                                school.end_date = study_end_date
                                school.save()
                            except Exception as e:
                                print(e.args)
                            # print(json.dumps(school.serialize(), indent=4, default=str))

                            initial['university'] = school.name
                            initial['degree'] = school.degree
                            initial['curso'] = school.major
                            initial['country_of_study'] = school.country
                            initial['city_of_study'] = school.city
                            initial['study_start_date'] = formart_date(school.start_date)
                            initial['study_end_date'] = formart_date(school.end_date)

                        form = UpdateTeacherForm(initial=initial)
                    else:
                        print(form.errors)
                else:
                    school_attended = teacher.school_attended.all()
                    
                    for school in school_attended:
                        initial['university'] = school.name
                        initial['degree'] = school.degree
                        initial['curso'] = school.major
                        initial['country_of_study'] = school.country
                        initial['city_of_study'] = school.city
                        initial['study_start_date'] = formart_date(school.start_date)
                        initial['study_end_date'] = formart_date(school.end_date)

                    form = UpdateTeacherForm(initial=initial)
                    
                return render(request,
                                'pages/teacher/teacher_profile_update_acc_info.html',
                                {'teacher': teacher, 'form': form})
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
def teacher_timetable(request, teacher_pk):
    if request.user.is_superuser:
        message = 'Acesso negado. Nao tem permissao para ver essa pagina.'
        return render(request,
					  'pages/auth/unauthorized.html',
					  {'message': message})
    
    if request.user.is_staff:
        teacher = TeacherNameNewModel.objects.filter(pk=teacher_pk)
        if teacher.exists():
            teacher = teacher.first()
            user = request.user
            if user == teacher.user:
                timetable = []
                year_name = None
                semester_name = None
                turma_name = None
                classe_name = None
                all_classes = []
                if request.method == 'POST':
                    form = TimeTableForm(request.POST)
                    if form.is_valid():
                        inner_data = form.cleaned_data
                        print(inner_data)
                        year = inner_data.get('year')
                        year_name = year
                        year = Year.objects.get(year=year)
                        turma = inner_data.get('turma')
                        turma_name = turma
                        turma = TurmaNewModel.objects.get(name=turma)
                        classe = inner_data.get('classe')
                        classe_name = classe
                        classe = ClasseNewModel.objects.get(name=classe)
                        semester = inner_data.get('semester')
                        semester_name = semester
                        semester = SemesterNewModel.objects.get(name=semester)
                        
                        timetable = TimeTable.objects.filter(
                            turma=turma,
                            classe=classe,
                            semester=semester,
                            year=year
                        )
                        if timetable.exists():
                            timetable = timetable.first()
                            subjects = timetable.subjects.all()
                            monday_classes = []
                            tuesday_classes = []
                            wednesday_classes = []
                            thursday_classes = []
                            friday_classes = []
                            for subject in subjects:
                                if subject.class_day == '2ª Feira':
                                    monday_classes.append(subject)
                                if subject.class_day == '3ª Feira':
                                    tuesday_classes.append(subject)
                                if subject.class_day == '4ª Feira':
                                    wednesday_classes.append(subject)
                                if subject.class_day == '5ª Feira':
                                    thursday_classes.append(subject)
                                if subject.class_day == '6ª Feira':
                                    friday_classes.append(subject)
                            
                            all_classes = [monday_classes, tuesday_classes, wednesday_classes,
                                        thursday_classes, friday_classes]
                            print(all_classes)
                        else:
                            timetable = []
                else:
                    form = TimeTableForm()
                
                return render(request,
                                'pages/teacher/teacher_timetable.html',
                                {'teacher': teacher, 'form': form, 'all_classes': all_classes,
                                 'year_name': year_name,
                                 'classe_name': classe_name,  'semester_name': semester_name,
                                 'turma_name': turma_name, 'all_classes': all_classes})
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
def teacher_marks(request, teacher_pk):
    if request.user.is_superuser:
        message = 'Acesso negado. Nao tem permissao para ver essa pagina.'
        return render(request,
					  'pages/auth/unauthorized.html',
					  {'message': message})
    
    if request.user.is_staff:
        teacher = TeacherNameNewModel.objects.filter(pk=teacher_pk)
        if teacher.exists():
            teacher = teacher.first()
            user = request.user
            if user == teacher.user:
                return render(request,
                                'pages/teacher/teacher_marks.html',
                                {'teacher': teacher})
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
def teacher_marks_all_view(request, teacher_pk):
    if request.user.is_superuser:
        message = 'Acesso negado. Nao tem permissao para ver essa pagina.'
        return render(request,
					  'pages/auth/unauthorized.html',
					  {'message': message})
    
    if request.user.is_staff:
        teacher = TeacherNameNewModel.objects.filter(pk=teacher_pk)
        if teacher.exists():
            teacher = teacher.first()
            user = request.user
            if user == teacher.user:
                year_name = None
                classe_name = None
                semester_name = None
                subject_name = None
                turma_name = None
                students = []
                student_marks = []
                test_names = []
                subject_names = []
                teacher_subjects = []
                has_marks = False
                if request.method == 'POST':
                    form = StudentAllMarkForm(request.POST)
                    if form.is_valid():
                        inner_data = form.cleaned_data
                        # print(inner_data)
                        year = inner_data.get('year')
                        year_name = year
                        year = Year.objects.get(year=year)
                        classe = inner_data.get('classe')
                        classe_name = classe
                        classe = urllib.parse.unquote(classe)
                        classe = ClasseNewModel.objects.get(name=classe.lower())
                        turma = inner_data.get('turma')
                        turma_name = turma
                        turma = TurmaNewModel.objects.get(name=turma)
                        semester = inner_data.get('semester')
                        semester_name = semester
                        semester = SemesterNewModel.objects.get(name=semester)

                        new_semester = SemesterModel.objects.filter(
                            name=semester,
                            turma=turma,
                            classe=classe,
                            year=year
                        )

                        # print(new_semester)
                        students = StudentNameNewModel.objects.filter(
                            new_semester__in=new_semester
                        )
                        # print(students)
                        teacher_subjects = []
                        if new_semester.exists():
                            new_semester = new_semester.first()

                            teacher_semesters = teacher.new_semester.all()
                            for teacher_sem in teacher_semesters:
                                if (teacher_sem.name == new_semester.name and 
                                    teacher_sem.year == new_semester.year and 
                                    teacher_sem.classe == new_semester.classe and
                                    teacher_sem.turma == new_semester.turma):
                                    teacher_subjects = teacher_sem.subjects.all()
                                    teacher_subjects = [subj.name for subj in teacher_subjects]
                                    
                            for student in students:
                                student_semesters = student.new_semester.all()
                                # stud_row = {
                                #     'first_name': student.first_name,
                                #     'last_name': student.last_name
                                # }
                                stud_row = [student.first_name, student.last_name]
                                # print(student_semesters)
                                for sem in student_semesters:
                                    if (sem.name == new_semester.name and 
                                        sem.year == new_semester.year and 
                                        sem.classe == new_semester.classe and
                                        sem.turma == new_semester.turma):
                                        student_subjects = sem.subjects.all()
                                        if student_subjects:
                                            for subj in student_subjects:
                                                if subj.name not in subject_names:
                                                    subject_names.append(subj.name)
                                                tests = subj.tests.all()
                                                # print([test.serialize() for test in tests])
                                                total = []
                                                for test in tests:
                                                    has_marks = True
                                                    total.append(test.mark)
                                                    # if test.name not in test_names:
                                                    #     test_names.append(test.name)
                                                    # stud_row[test.name.replace(' ', '_')] = test.mark
                                                try:
                                                    media = round(sum(total) / len(total), 1)
                                                    # stud_row['media'] = media
                                                    stud_row.append(media)
                                                except Exception as e:
                                                    # stud_row['media'] = 0
                                                    stud_row.append(0) 
                                        
                                    else:
                                        print('Semesters not equal')
                                        # pass
                                try:
                                    # print(stud_row)
                                    final_mark = stud_row[2:]
                                    print(final_mark)
                                    final_mark = sum(final_mark) / len(final_mark)
                                    stud_row.append(round(final_mark, 1))
                                except Exception as e:
                                    stud_row.append(0)
                                student_marks.append(stud_row)
                    else:
                        print(form.errors)
                else:
                    form = StudentAllMarkForm()

                return render(request,
                                'pages/teacher/teacher_marks_all_view.html',
                                {'teacher': teacher, 'form': form, 'student_marks': student_marks,
                                 'test_names': test_names, 'year_name': year_name,
                                 'semester_name': semester_name, 'classe_name': classe_name,
                                 'turma_name': turma_name, 'subject_name': subject_name,
                                 'has_marks': has_marks, 'subject_names': subject_names})
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
def teacher_marks_view(request, teacher_pk):
    if request.user.is_superuser:
        message = 'Acesso negado. Nao tem permissao para ver essa pagina.'
        return render(request,
					  'pages/auth/unauthorized.html',
					  {'message': message})
    
    if request.user.is_staff:
        teacher = TeacherNameNewModel.objects.filter(pk=teacher_pk)
        if teacher.exists():
            teacher = teacher.first()
            user = request.user
            if user == teacher.user:
                year_name = None
                classe_name = None
                semester_name = None
                subject_name = None
                turma_name = None
                students = []
                student_marks = []
                test_names = []
                teacher_subjects = []
                has_marks = False
                if request.method == 'POST':
                    form = StudentMarkForm(request.POST)
                    if form.is_valid():
                        inner_data = form.cleaned_data
                        # print(inner_data)
                        year = inner_data.get('year')
                        year_name = year
                        year = Year.objects.get(year=year)
                        classe = inner_data.get('classe')
                        classe_name = classe
                        classe = urllib.parse.unquote(classe)
                        classe = ClasseNewModel.objects.get(name=classe.lower())
                        turma = inner_data.get('turma')
                        turma_name = turma
                        turma = TurmaNewModel.objects.get(name=turma)
                        semester = inner_data.get('semester')
                        semester_name = semester
                        semester = SemesterNewModel.objects.get(name=semester)
                        subject_name = inner_data.get('subject')
                        subject = SubjectNameNewModel.objects.filter(name=subject_name)
                        if subject.exists():
                            subject = subject.first()

                            new_semester = SemesterModel.objects.filter(
                                name=semester,
                                turma=turma,
                                classe=classe,
                                year=year
                            )

                            # print(new_semester)
                            students = StudentNameNewModel.objects.filter(
                                new_semester__in=new_semester
                            )
                            # print(students)
                            teacher_subjects = []
                            if new_semester.exists():
                                new_semester = new_semester.first()

                                teacher_semesters = teacher.new_semester.all()
                                for teacher_sem in teacher_semesters:
                                    if (teacher_sem.name == new_semester.name and 
                                        teacher_sem.year == new_semester.year and 
                                        teacher_sem.classe == new_semester.classe and
                                        teacher_sem.turma == new_semester.turma):
                                        teacher_subjects = teacher_sem.subjects.all()
                                        teacher_subjects = [subj.name for subj in teacher_subjects]
                                        
                                # print(new_semester)
                                for student in students:
                                    student_semesters = student.new_semester.all()
                                    stud_row = {
                                        'first_name': student.first_name,
                                        'last_name': student.last_name
                                    }
                                    # print(student_semesters)
                                    for sem in student_semesters:
                                        if (sem.name == new_semester.name and 
                                            sem.year == new_semester.year and 
                                            sem.classe == new_semester.classe and
                                            sem.turma == new_semester.turma):
                                            student_subjects = sem.subjects.all()
                                            # print(subjects)
                                            # print('Semester equal')
                                            if student_subjects:
                                                for subj in student_subjects:
                                                    if subj.name in teacher_subjects:
                                                        # print(subj.name, subject, subj.name == subject)
                                                        # print(type(subj.name), type(subject))
                                                        if subj.name == subject:
                                                            # print(student, ':', subj.name, end=', ')
                                                            tests = subj.tests.all()
                                                            total = []
                                                            for test in tests:
                                                                has_marks = True
                                                                total.append(test.mark)
                                                                if test.name not in test_names:
                                                                    test_names.append(test.name)
                                                                # print(test, end=', ')
                                                                stud_row[test.name.replace(' ', '_')] = test.mark
                                                            # print()
                                                            try:
                                                                media = sum(total) / len(total)
                                                                stud_row['media'] = round(media, 1)
                                                            except Exception as e:
                                                                stud_row['media'] = 0
                                            else:
                                                print(f'{subject} not registed to {student} yet')
                                        else:
                                            print('Semesters not equal')
                                            # pass
                                    # print(stud_row)
                                    student_marks.append(stud_row)
                            else:
                                print(f'Semester does not exist')
                    else:
                        print(form.errors)
                else:
                    form = StudentMarkForm()

                return render(request,
                                'pages/teacher/teacher_marks_view.html',
                                {'teacher': teacher, 'form': form, 'student_marks': student_marks,
                                 'test_names': test_names, 'year_name': year_name,
                                 'semester_name': semester_name, 'classe_name': classe_name,
                                 'turma_name': turma_name, 'subject_name': subject_name,
                                 'has_marks': has_marks})
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
    

@require_POST
def teacher_add_marks_api(request):
    data = json.loads(request.body)
    # print(data)
    for row in data:
        try:
            year_name = row['year-name']
            year = Year.objects.get(year=year_name)
            semester_name = row['semester-name']
            semester = SemesterNewModel.objects.get(name=semester_name)
            classe_name = row['classe-name']
            classe = ClasseNewModel.objects.get(name=classe_name)
            turma_name = row['turma-name']
            turma = TurmaNewModel.objects.get(name=turma_name)
            mark = row['mark']
            test_name = row['test-name']
            subject = SubjectNameNewModel.objects.get(name=row['subject'])
            new_semester = SemesterModel.objects.filter(
                name=semester,
                turma=turma,
                classe=classe,
                year=year
            )
            # print(new_semester)
            if new_semester.exists():
                new_semester = new_semester.first()
                student = StudentNameNewModel.objects.get(pk=row['student-pk'])
                student_semesters = student.new_semester.all()
                for sem in student_semesters:
                    if (sem.name == new_semester.name and sem.year == new_semester.year and
                        sem.classe == new_semester.classe and sem.turma == new_semester.turma):
                        subjects = sem.subjects.all()
                        if subjects:
                            if subject not in [sub.name for sub in subjects]:
                                subject_mark = SubjectTestsNewModel.objects.create(
                                    name=subject
                                )
                                subject_mark.save()
                                test = TestNewModel.objects.create(
                                    name=test_name,
                                    mark=mark
                                )
                                test.save()
                                print('Created test mark')
                                subject_mark.tests.add(test)
                                subject_mark.save()
                                sem.subjects.add(subject_mark)
                                sem.save()
                                print('Created test mark to subjec')
                            else:
                                for subj in subjects:
                                    if subj.name == subject:
                                        # tests = subj.tests.all()
                                        # print(type(subj))
                                        try:
                                            test = TestNewModel.objects.create(
                                                name=test_name,
                                                mark=mark
                                            )
                                            test.save()
                                            print('Added test mark')
                                            subj.tests.add(test)
                                            subj.save()
                                            print('Added test mark to subjec')
                                        except Exception as e:
                                            print(e.args)

                        else:
                            subject_mark = SubjectTestsNewModel.objects.create(
                                name=subject
                            )
                            subject_mark.save()
                            test = TestNewModel.objects.create(
                                name=test_name,
                                mark=mark
                            )
                            test.save()
                            print('Created test mark')
                            subject_mark.tests.add(test)
                            subject_mark.save()
                            sem.subjects.add(subject_mark)
                            sem.save()
                            print('Created test mark to subjec')

                        # print('Same semesters')
                    else:
                        # print('Different semesters')
                        pass
        except Exception as e:
            print(e.args)
            student = None

    return JsonResponse({
        'correct_code': True
    })

@login_required
def teacher_marks_add_manually(request, teacher_pk):
    if request.user.is_superuser:
        message = 'Acesso negado. Nao tem permissao para ver essa pagina.'
        return render(request,
					  'pages/auth/unauthorized.html',
					  {'message': message})
    
    if request.user.is_staff:
        teacher = TeacherNameNewModel.objects.filter(pk=teacher_pk)
        if teacher.exists():
            teacher = teacher.first()
            user = request.user
            print(user, teacher.user, user == teacher.user)
            if user == teacher.user:
                year_name = None
                classe_name = None
                semester_name = None
                turma_name = None
                students = []
                teacher_subjects = []
                if request.method == 'POST':
                    form = AddStudentMarkForm(request.POST)
                    if form.is_valid():
                        inner_data = form.cleaned_data
                        # print(inner_data)
                        year = inner_data.get('year')
                        year_name = year
                        year = Year.objects.get(year=year)
                        classe = inner_data.get('classe')
                        classe_name = classe
                        classe = urllib.parse.unquote(classe)
                        classe = ClasseNewModel.objects.get(name=classe.lower())
                        turma = inner_data.get('turma')
                        turma_name = turma
                        turma = TurmaNewModel.objects.get(name=turma)
                        semester = inner_data.get('semester')
                        semester_name = semester
                        semester = SemesterNewModel.objects.get(name=semester)

                        new_semester = SemesterModel.objects.filter(
                            name=semester,
                            turma=turma,
                            classe=classe,
                            year=year
                        )
                        # print(new_semester)
                        students = StudentNameNewModel.objects.filter(
                            new_semester__in=new_semester
                        )
                        # print(students)

                        teacher_semesters = teacher.new_semester.all()
                        for sem in teacher_semesters:
                            semester = new_semester.first()
                            try:
                                if (sem.name == semester.name and sem.turma == semester.turma and
                                    sem.turma == semester.turma):
                                    subjects = sem.subjects.all()
                                    for subj in subjects:
                                        if subj not in teacher_subjects:
                                            teacher_subjects.append(subj)
                            except Exception as e:
                                print(e.args)
                    else:
                        print(form.errors)
                else:
                    form = AddStudentMarkForm()

                return render(request,
                                'pages/teacher/teacher_marks_add_manually.html',
                                {'teacher': teacher, 'form': form, 'students': students,
                                 'teacher_subjects': teacher_subjects, 'year_name': year_name,
                                 'semester_name': semester_name, 'classe_name': classe_name,
                                 'turma_name': turma_name})
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
def teacher_marks_add_from_file(request, teacher_pk):
    if request.user.is_superuser:
        message = 'Acesso negado. Nao tem permissao para ver essa pagina.'
        return render(request,
					  'pages/auth/unauthorized.html',
					  {'message': message})
    
    if request.user.is_staff:
        teacher = TeacherNameNewModel.objects.filter(pk=teacher_pk)
        if teacher.exists():
            teacher = teacher.first()
            user = request.user
            if user == teacher.user:
                students = []
                test_name = None
                has_errors = False
                teacher_subjects = []
                if request.method == 'POST':
                    form = AddStudentMarkFromFileForm(request.POST, request.FILES)
                    if form.is_valid():
                        inner_data = form.cleaned_data
                        year = inner_data.get('year')
                        year = Year.objects.get(year=year)
                        classe = inner_data.get('classe')
                        classe = urllib.parse.unquote(classe)
                        classe = ClasseNewModel.objects.get(name=classe.lower())
                        turma = inner_data.get('turma')
                        turma = TurmaNewModel.objects.get(name=turma)
                        subject = inner_data.get('subject')
                        test_name = inner_data.get('test')
                        semester = inner_data.get('semester')
                        semester_name = SemesterNewModel.objects.get(name=semester)

                        new_semester = SemesterModel.objects.filter(
                            name=semester_name,
                            turma=turma,
                            classe=classe,
                            year=year
                        )
                        if new_semester.exists():
                            new_semester = new_semester.first()
                        
                            uploaded_file = request.FILES['file']
                            # print(uploaded_file)
                            fs = FileSystemStorage()
                            filename = fs.save(uploaded_file.name, uploaded_file)
                            # print(filename)
                            path = os.path.join(os.getcwd(), 'media', filename)
                            # print(path)
                            df = None
                            if path.endswith('xlsx'):
                                df = pd.read_excel(path)
                            if path.endswith('csv'):
                                df = pd.read_csv(path)

                            print(df.head())
                            for row in df.itertuples():
                                first_name = row.first_name
                                last_name = row.last_name
                                mark = row.test
                                row = {
                                    'first_name': first_name,
                                    'last_name': last_name,
                                    'mark': mark
                                }
                                students.append(row)

                                student = StudentNameNewModel.objects.filter(
                                    first_name=first_name,
                                    last_name=last_name
                                )
                                print(new_semester)
                                if student.exists():
                                    student = student.first()

                                    student_semesters = student.new_semester.all()
                                    for sem in student_semesters:
                                        if (sem.name == new_semester.name and 
                                            sem.year == new_semester.year and 
                                            sem.classe == new_semester.classe and
                                            sem.turma == new_semester.turma):
                                            subjects = sem.subjects.all()
                                            if subjects:
                                                if subject not in [sub.name for sub in subjects]:
                                                    subject_mark = SubjectTestsNewModel.objects.create(
                                                        name=subject
                                                    )
                                                    subject_mark.save()
                                                    test = TestNewModel.objects.create(
                                                        name=test_name,
                                                        mark=mark
                                                    )
                                                    test.save()
                                                    print('Created test mark')
                                                    subject_mark.tests.add(test)
                                                    subject_mark.save()
                                                    sem.subjects.add(subject_mark)
                                                    sem.save()
                                                    print('Created test mark to subjec')
                                                else:
                                                    for subj in subjects:
                                                        if subj.name == subject:
                                                            # tests = subj.tests.all()
                                                            # print(type(subj))
                                                            try:
                                                                test = TestNewModel.objects.create(
                                                                    name=test_name,
                                                                    mark=mark
                                                                )
                                                                test.save()
                                                                print('Added test mark')
                                                                subj.tests.add(test)
                                                                subj.save()
                                                                print('Added test mark to subjec')
                                                            except Exception as e:
                                                                print(e.args)

                                            else:
                                                subject_mark = SubjectTestsNewModel.objects.create(
                                                    name=subject
                                                )
                                                subject_mark.save()
                                                test = TestNewModel.objects.create(
                                                    name=test_name,
                                                    mark=mark
                                                )
                                                test.save()
                                                print('Created test mark')
                                                subject_mark.tests.add(test)
                                                subject_mark.save()
                                                sem.subjects.add(subject_mark)
                                                sem.save()
                                                print('Created test mark to subjec')
                    else:
                        print(form.errors)
                        has_errors = True
                else:
                    form = AddStudentMarkFromFileForm()
                return render(request,
                                'pages/teacher/teacher_marks_add_from_file.html',
                                {'teacher': teacher, 'form': form, 'students': students,
                                 'teacher_subjects': teacher_subjects, 'has_errors': has_errors,
                                 'students': students, 'test_name': test_name})
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
def teacher_presencas(request, teacher_pk):
    if request.user.is_superuser:
        message = 'Acesso negado. Nao tem permissao para ver essa pagina.'
        return render(request,
					  'pages/auth/unauthorized.html',
					  {'message': message})
    
    if request.user.is_staff:
        teacher = TeacherNameNewModel.objects.filter(pk=teacher_pk)
        if teacher.exists():
            teacher = teacher.first()
            user = request.user
            if user == teacher.user:
                return render(request,
                                'pages/teacher/teacher_presencas.html',
                                {'teacher': teacher})
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
def teacher_view_attendance(request, teacher_pk):
    if request.user.is_superuser:
        message = 'Acesso negado. Nao tem permissao para ver essa pagina.'
        return render(request,
					  'pages/auth/unauthorized.html',
					  {'message': message})
    
    if request.user.is_staff:
        teacher = TeacherNameNewModel.objects.filter(pk=teacher_pk)
        if teacher.exists():
            teacher = teacher.first()
            user = request.user
            if user == teacher.user:
                attendances = []
                if request.method == 'POST':
                    form = StudentAttendanceForm(request.POST)
                    if form.is_valid():
                        inner_data = form.cleaned_data
                        print(inner_data)
                        year = inner_data.get('year')
                        year = Year.objects.get(year=year)
                        classe = inner_data.get('classe')
                        classe = urllib.parse.unquote(classe)
                        classe = ClasseNewModel.objects.get(name=classe.lower())
                        turma = inner_data.get('turma')
                        turma = TurmaNewModel.objects.get(name=turma)
                        month = inner_data.get('month')
                        print(month)
                        semester = inner_data.get('semester')
                        semester_name = SemesterNewModel.objects.get(name=semester)

                        new_semester = SemesterModel.objects.filter(
                            name=semester_name,
                            turma=turma,
                            classe=classe,
                            year=year
                        )
                        # print(new_semester)
                        semester = None
                        if new_semester.exists():
                            semester = new_semester.first()

                            teacher_semesters = teacher.new_semester.all()
                            teacher_sems = []
                            subjects = []
                            for sem in teacher_semesters:
                                if (sem.name == semester.name and 
                                    sem.classe == semester.classe and sem.turma == semester.turma):
                                    subjects = [subj.name for subj in sem.subjects.all()]

                            students = StudentNameNewModel.objects.filter(
                                new_semester__in=new_semester
                            )
                            today = datetime.today()
                            year, month, day = today.strftime('%Y-%m-%d').split('-')
                            for student in students:
                                for subject in subjects:
                                    attendance = StudentAttendance.objects.filter(
                                        student=student,
                                        subject=subject,
                                        semester=semester_name,
                                        class_datetime__year=year,
                                        class_datetime__month=month,
                                        class_datetime__day=day
                                    )
                                    if attendance.exists():
                                        attendance = attendance.first()
                                        attendances.append(attendance)
                        # print(students)
                        
                    else:
                        print(form.errors)
                else:
                    form = StudentAttendanceForm()

                return render(request,
                                'pages/teacher/teacher_view_attendance.html',
                                {'teacher': teacher, 'form': form, 'attendances': attendances})
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
def teacher_take_presencas(request, teacher_pk):
    if request.user.is_superuser:
        message = 'Acesso negado. Nao tem permissao para ver essa pagina.'
        return render(request,
					  'pages/auth/unauthorized.html',
					  {'message': message})
    
    if request.user.is_staff:
        teacher = TeacherNameNewModel.objects.filter(pk=teacher_pk)
        if teacher.exists():
            teacher = teacher.first()
            user = request.user
            if user == teacher.user:
                return render(request,
                                'pages/teacher/teacher_take_presencas.html',
                                {'teacher': teacher})
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
def attandance_qrcode(request, teacher_pk, student_pk, year, semester, classe, turma, subject):
    # url = f'http://localhost:8000/professor-presenca-form/{teacher_pk}/{student_pk}/{year}/{semester}/{classe}/{turma}/{subject}/'
    # img = segno.make(url)
    # filename = f'/media/presencas/qrcode-{teacher_pk}-{student_pk}-{year}-{semester}-{classe}-{turma}-{subject}.png'
    # img.save(f'.{filename}',
    #     # border=5, 
    #     # scale=10,
    #     # dark='darkred',
    #     # light='lightblue',
    #     # dark='#0000ffcc',

    #     dark='darkblue',
    #     data_dark='steelblue',
    #     scale=5
    # )
    # qrcode = AttendanceQRcode.objects.create()
    classe = classe.replace('ª ', '_')
    qrcode = f'qrcode_{teacher_pk}_{student_pk}_{year}_{semester}_{classe}_{turma}_{subject}.png'
    print(qrcode)
    return render(request,
                  'pages/teacher/attandance_qrcode.html',
                  {'qrcode': qrcode})



@login_required
def teacher_record_attendance(request, teacher_pk, student_pk, year, semester, classe, turma, subject, attended):
    student = StudentNameNewModel.objects.get(pk=student_pk)
    teacher = TeacherNameNewModel.objects.get(pk=teacher_pk)
    # print(attended)
    if attended == 'Presente':
        attended = True
    elif attended == 'Ausente':
        attended = False
    # print(attended)
    print(f'SUBJECT: {subject}')

    year = Year.objects.get(year=year)
    classe = urllib.parse.unquote(classe)
    classe = ClasseNewModel.objects.get(name=classe.lower())
    turma = TurmaNewModel.objects.get(name=turma)
    subject = SubjectNameNewModel.objects.get(name=subject)
    semester_name = SemesterNewModel.objects.get(name=semester)
    new_semester = SemesterModel.objects.filter(
        name=semester_name,
        turma=turma,
        classe=classe,
        year=year
    )

    attended_exists = False
    teacher_sujects = []
    if new_semester.exists():
        new_semester = new_semester.first()
        # print(new_semester)
        stud_semesters = student.new_semester.all()
        # print(stud_semesters)

        for sem in teacher.new_semester.all():
            if check_semesters_are_equal(sem, new_semester):
                for subj in sem.subjects.all():
                    if subj not in teacher_sujects:
                        teacher_sujects.append(subj.name)
                        
        for sem in stud_semesters:
            if check_semesters_are_equal(sem, new_semester):
                subjects = sem.subjects.all()
                for subj in subjects:
                    # print(subj)
                    print(subj.name, subject, subj.name == subject)
                    if subj.name == subject:
                        today = datetime.today()
                        current_year, month, day = today.strftime('%Y-%m-%d').split('-')

                        attendance = StudentAttendance.objects.filter(
                            student=student,
                            semester=semester_name,
                            subject=subject,
                            class_datetime__year=current_year,
                            class_datetime__month=month,
                            class_datetime__day=day
                        )
                        print(attendance)
                         
                        if attendance.exists():
                            attended_exists = True
                            attendance = attendance.first()
                            attendance.class_datetime = today
                            attendance.attended = attended
                            attendance.save() 
                            print('Attendance exists')
                        else:
                            attendance = StudentAttendance.objects.create(
                                student=student,
                                teacher=teacher,
                                year=year,
                                semester=semester_name,
                                classe=classe,
                                turma=turma,
                                subject=subject,
                                attended=attended
                            )
                            attendance.save()
                            subj.attendance.add(attendance)
                            subj.save()
                            print('Captured new attendance.')
                    else:
                        print('Subjects are different')
    else:
        print('Semester does not exist')                        
    return JsonResponse({
        'attended': attended,
        'student_name': student.fullname(),
        'attended_exists': attended_exists
    })


@login_required
def attandance_form(request, teacher_pk, student_pk, year, semester, classe, turma, subject):
    link_is_not_open = False
    message = None
    greeting = ''
    new_attandace_token = False
    attandace_is_already_token = False
    try:
        student = StudentNameNewModel.objects.get(pk=student_pk)
        teacher = TeacherNameNewModel.objects.get(pk=teacher_pk)

        try:
            student_user = request.user
            print(student_user)
            student_user = student_user.studentnamenewmodel_set.all()
            print(student_user)
            if student_user.exists():
                student_user = student_user.first()
                if student_user == student:
                    year = Year.objects.get(year=year)
                    classe = urllib.parse.unquote(classe)
                    classe = ClasseNewModel.objects.get(name=classe.lower())
                    # print(classe)
                    turma = TurmaNewModel.objects.get(name=turma)
                    subject = SubjectNameNewModel.objects.get(name=subject)
                    semester_name = SemesterNewModel.objects.get(name=semester)

                    new_semester = SemesterModel.objects.filter(
                        name=semester_name,
                        turma=turma,
                        classe=classe,
                        year=year
                    )
                    print(new_semester)
                    if new_semester.exists():
                        new_semester = new_semester.first()
                        stud_semesters = student.new_semester.all()
                        for sem in stud_semesters:
                            for subj in sem.subjects.all():
                                if subj.name == subject:
                                    today = datetime.today()
                                    year, month, day = today.strftime('%Y-%m-%d').split('-')
                                    hour = today.hour
                                    if hour < 12:
                                        greeting = 'Bom dia'
                                    else:
                                        greeting = 'Boa tarde'

                                    if subj.link_is_open:
                                        print('Link is open')
                                        attendance = StudentAttendance.objects.filter(
                                            student=student,
                                            semester=semester_name,
                                            subject=subject,
                                            class_datetime__year=year,
                                            class_datetime__month=month,
                                            class_datetime__day=day
                                        )
                                        print(attendance)
                                        
                                        if attendance.exists():
                                            message = f'{greeting} {student.fullname()}, nao pode confirmar sua presença duas vezes, obrigado.'
                                            attandace_is_already_token = True
                                        else:
                                            attendance = StudentAttendance.objects.create(
                                                student=student,
                                                semester=semester_name,
                                                subject=subject,
                                                attended=True
                                            )
                                            attendance.save()
                                            subj.attendance.add(attendance)
                                            subj.save()
                                            new_attandace_token = True
                                            message = f'{greeting} {student.fullname()}, já confirmaste a sua presença na aula com sucesso.'
                                    else:
                                        link_is_not_open = True
                                        print('Link is not open')
                else:
                    logout(request)
                    previous_path = request.META.get('HTTP_REFERER')
                    return redirect(previous_path)
        except Exception as e:
            print(e)
    except Exception as e:
        print(e.args)
        student = None
        subject = None

    return render(request,
                  'pages/teacher/attandance_form.html',
                  {'student': student, 'subject': subject, 'link_is_not_open': link_is_not_open,
                   'message': message, 'attandace_is_already_token': attandace_is_already_token,
                   'new_attandace_token': new_attandace_token, 'greeting': greeting})


@login_required
def teacher_take_presencas_by_list(request, teacher_pk):
    if request.user.is_superuser:
        message = 'Acesso negado. Nao tem permissao para ver essa pagina.'
        return render(request,
					  'pages/auth/unauthorized.html',
					  {'message': message})
    
    if request.user.is_staff:
        teacher = TeacherNameNewModel.objects.filter(pk=teacher_pk)
        students = []
        teacher_sujects = []
        student_info = []
        subject = 'None'
        if teacher.exists():
            teacher = teacher.first()
            user = request.user
            if user == teacher.user:
                year_name = None
                semester_name = None
                turma_name = None
                classe_name = None
                message = False
                subject_not_belong_to_teacher = False

                form = AttentanceForm(request.POST)
                if form.is_valid():
                    inner_data = form.cleaned_data
                    # print(inner_data)
                    year = inner_data.get('year')
                    year_name = year
                    year = Year.objects.get(year=year)
                    turma = inner_data.get('turma')
                    turma_name = turma
                    turma = TurmaNewModel.objects.get(name=turma)
                    classe = inner_data.get('classe')
                    classe_name = classe
                    classe = ClasseNewModel.objects.get(name=classe)
                    semester = inner_data.get('semester')
                    semester_name = semester
                    semester = SemesterNewModel.objects.get(name=semester)
                    subject_name = inner_data.get('subject') 
                    if subject_name is None:
                        message = True
                        # print('Subject not selected')
                    else:
                        # print('Subject selected')
                        subject = SubjectNameNewModel.objects.filter(name=subject_name)
                        if subject.exists():
                            subject = subject.first()
                    
                    new_semester = SemesterModel.objects.filter(
                        name=semester,
                        turma=turma,
                        classe=classe,
                        year=year
                    )
                    # print(new_semester)
                    students = StudentNameNewModel.objects.filter(
                        new_semester__in=new_semester
                    )
                    students = students.order_by('first_name')
                    
                    if new_semester.exists():
                        new_semester = new_semester.first()

                        for sem in teacher.new_semester.all():
                            if check_semesters_are_equal(sem, new_semester):
                                for subj in sem.subjects.all():
                                    if subj not in teacher_sujects:
                                        teacher_sujects.append(subj.name)
            
                        print(subject in teacher_sujects)
                        try:
                            if subject not in teacher_sujects:
                                subject_not_belong_to_teacher = True
                                # print('subject_not_belong_to_teacher'.upper())
                        except Exception as e:
                            # print('subject_belong_to_teacher'.upper())
                            pass
 
                        for student in students:
                            row = {}
                            row['pk'] = student.pk
                            row['first_name'] = student.first_name
                            row['last_name'] = student.last_name

                            today = datetime.today()
                            year, month, day = today.strftime('%Y-%m-%d').split('-')
                            student_semesters = student.new_semester.all()
                            for stud_sem in student_semesters:
                                if check_semesters_are_equal(stud_sem, new_semester):
                                    subjects = stud_sem.subjects.all()
                                    for subj in subjects:
                                        if subj.name == subject:
                                            if subj.name in teacher_sujects:
                                                attendance = StudentAttendance.objects.filter(
                                                    student=student,
                                                    semester=semester,
                                                    subject=subj.name,
                                                    class_datetime__year=year,
                                                    class_datetime__month=month,
                                                    class_datetime__day=day
                                                )
                                                # print(attendance)
                                                if attendance.exists():
                                                    attendance = attendance.first()
                                                    # print(attendance.serialize())
                                                    row['attended'] = attendance.attended
                                                    # student_info.append(attendance.serialize())
                            # print(row)
                            student_info.append(row)
                        # print(student_info)
                else:
                    form = AttentanceForm()

                print(subject)

                return render(request,
                                'pages/teacher/teacher_take_presencas_by_list.html',
                                {'teacher': teacher, 'form': form, 'students': student_info,
                                 'teacher_sujects': teacher_sujects, 'message': message,
                                 'year_name': year_name, 'classe_name': classe_name,
                                 'semester_name': semester_name, 'turma_name': turma_name,
                                 'subject': subject,
                                 'subject_not_belong_to_teacher': subject_not_belong_to_teacher})
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
def teacher_take_presencas_by_qrcode(request, teacher_pk):
    if request.user.is_superuser:
        message = 'Acesso negado. Nao tem permissao para ver essa pagina.'
        return render(request,
					  'pages/auth/unauthorized.html',
					  {'message': message})
    
    if request.user.is_staff:
        teacher = TeacherNameNewModel.objects.filter(pk=teacher_pk)
        if teacher.exists():
            teacher = teacher.first()
            user = request.user
            if user == teacher.user:
                return render(request,
                                'pages/teacher/teacher_take_presencas_by_qrcode.html',
                                {'teacher': teacher})
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
def teacher_homepage(request, teacher_pk):
    if request.user.is_superuser:
        message = 'Acesso negado. Nao tem permissao para ver essa pagina.'
        return render(request,
					  'pages/auth/unauthorized.html',
					  {'message': message})
    
    if request.user.is_staff:
        teacher = TeacherNameNewModel.objects.filter(pk=teacher_pk)
        if teacher.exists():
            teacher = teacher.first()
            user = request.user
            if user == teacher.user:
                return render(request,
                                'pages/teacher/teacher_homepage.html',
                                {'teacher': teacher})
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

    

