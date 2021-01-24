from django.contrib import admin

# Register your models here.

from .models import Student, Faculty, Department, Course, Takes, Section, Teaches

admin.site.register(Student)
admin.site.register(Faculty)
admin.site.register(Department)
admin.site.register(Course)
admin.site.register(Takes)
admin.site.register(Section)
admin.site.register(Teaches)