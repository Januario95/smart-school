from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import (
    SemesterNewModel, ClasseNewModel, TurmaNewModel,
    TestNewModel, StudentNameNewModel, SubjectNewModel,
    SubjectNameNewModel, Year, SemesterModel, SubjectTestsNewModel,
    ParentNameNewModel, TeacherNameNewModel, StudentMessageAdmin,
    ParentToAdminMessage, AdminToParentsMessage, AdminToTeacherMessage,
    Attendance, SubjectTimetable, TimeTable, 
    TeacherClassAttendance, TeacherSchoolAttended, StudentAttendance,
    AttendanceQRcode, TeacherAndStudentMessage,
)


@admin.register(TeacherAndStudentMessage)
class TeacherAndStudentMessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'sender', 'receiver', 'message', 'sent_at', 'resent_at')

@admin.register(AttendanceQRcode)
class AttendanceQRcodeAdmin(admin.ModelAdmin):
    list_display = ('id', 'image')

@admin.register(StudentAttendance)
class StudentAttendanceAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'teacher', 'year', 'semester', 'classe', 'turma',
                    'subject', 'class_datetime', 'attended', 'comment')

@admin.register(TeacherSchoolAttended)
class TeacherSchoolAttendedAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'city', 'country', 'degree',
                    'major', 'start_date', 'end_date')

@admin.register(TeacherClassAttendance)
class TeacherClassAttendanceAdmin(admin.ModelAdmin):
    list_display = ('id', 'teacher', 'turma', 'classe', 'subject',
                    'class_date', 'class_time', 'attended')
    # filter_horizontal = ('teacher',) # msust be many-to-many
    list_filter = ('turma', 'classe')
    list_editable = ('class_date', 'class_time')

@admin.register(TimeTable)
class TimeTableAdmin(admin.ModelAdmin):
    list_display = ('id', 'turma', 'classe', 'year', 'semester')

@admin.register(SubjectTimetable)
class SubjectTimetableAdmin(admin.ModelAdmin):
    list_display = ('id', 'subject_name', 'class_day', 'class_start_time', 'class_end_time')

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('id', 'teacher', 'student', 'semester', 'reason', 'is_present', 'class_time')

@admin.register(AdminToTeacherMessage)
class AdminToTeacherMessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'sender', 'receiver', 'message', 'sent_at')

@admin.register(AdminToParentsMessage)
class AdminToParentMessageModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'sender', 'receiver', 'message', 'sent_at')

@admin.register(ParentToAdminMessage)
class ParentToAadminMessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'sender', 'receiver', 'message', 'sent_at')

@admin.register(StudentMessageAdmin)
class StudentMessageModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'sender', 'receiver', 'message', 'sent_at')
    # list_editable = ('message',)
    # search_fields = ('receiver',)

@admin.register(SubjectTestsNewModel)
class SubjectTestsNewModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'link_is_open')
    list_editable = ('link_is_open',)
    list_per_page = 700

@admin.register(SemesterModel)
class SemesterModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'turma', 'classe', 'year', 'created_at', 'updated_at')
    list_per_page = 700

@admin.register(Year)
class YearAdmin(admin.ModelAdmin):
    list_display = ('id', 'year')

@admin.register(SemesterNewModel)
class SemesterNewModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'year')
	

@admin.register(ClasseNewModel)
class ClasseNewModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    
@admin.register(TurmaNewModel)
class TurmaNewModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

@admin.register(TestNewModel)
class TestNewModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'mark')
    list_per_page = 700

@admin.register(SubjectNewModel)
class SubjectNewModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'turma', 'classe', 'semester')
    list_per_page = 700
    list_filter = ('turma', 'classe', 'semester')

@admin.register(SubjectNameNewModel)
class SubjectNameNewModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_per_page = 700

@admin.register(StudentNameNewModel)
class StudentNameNewModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 
                    'profile_pic_',
                    'numero_de_bi',
                    'gender', 'birth_date', 'phone_number', 'email',
                    'province', 'city', 'bairro',
                    # 'turma', 'classe', 'semester', 
                    'year_', 'created_at', 'updated_at')
    # list_filter = ('turma', 'classe', 'semester')
    list_display_links = ('id', 'first_name')
    list_per_page = 700

    def profile_pic_(self, obj):
        profile_pic = obj.profile_pic
        img = mark_safe(f'''
            <img src="/media/{ profile_pic }" style="width:100px;height:100px;border-radius:50%;" />
        ''')
        return img
    profile_pic_.short_description = 'Image de perfil'


    def year_(self, obj):
        years = obj.year.all()
        ol = '<ol>'
        for year in years:
            ol += f'<li>{year}</li>'
        ol += '</li>'
        return mark_safe(ol)
    year_.short_description = 'Year'


@admin.register(TeacherNameNewModel)
class TeacherNameNewModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 
                    'profile_pic_',
                    'gender', 
                    'phone_number', 'email',
                    'province', 'city', 'bairro', 'created_at', 'updated_at')
    list_display_links = ('id', 'first_name')
    list_per_page = 700
    list_filter = ('gender',)
    # list_editable = ('subjects',)

    def profile_pic_(self, obj):
        profile_pic = obj.profile_pic
        img = mark_safe(f'''
            <img src="/media/{ profile_pic }" style="width:100px;height:100px;border-radius:50%;" />
        ''')
        return img
    profile_pic_.short_description = 'Image de perfil'


@admin.register(ParentNameNewModel)
class ParentNameNewModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'gender', 
                    'phone_number', 'email', 'job_title',
                    'province', 'city', 'bairro', 'created_at', 'updated_at')
    list_per_page = 700
    list_filter = ('gender',)
















