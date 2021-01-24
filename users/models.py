from django.db import models

# Create your models here.

class Student(models.Model):
    stdId = models.PositiveIntegerField()
    name = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    schoolName = models.CharField(max_length=100)
    gender = models.CharField(max_length=10)
    dob = models.DateField()

class Faculty(models.Model):
    facultyId = models.PositiveIntegerField()
    name = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    gender = models.CharField(max_length=10)
    salary = models.PositiveIntegerField()

class Department(models.Model):
    department= models.CharField(max_length=30)
    school=models.CharField(max_length=40)

class Course(models.Model):
    crsCode =models.CharField(max_length=100)
    crsName =models.CharField(max_length=100)
    department=models.CharField(max_length=100)
    credit=models.PositiveIntegerField()

class Takes (models.Model):
    stdId=models.PositiveIntegerField()
    crsCode=models.CharField(max_length=100)
    secId=models.PositiveIntegerField()
    semester=models.CharField(max_length=20)
    year=models.PositiveIntegerField()
    ploID=models.PositiveIntegerField()
    cloID=models.PositiveIntegerField()
    marks=models.DecimalField(max_digits=5, decimal_places=2)

class Section (models.Model):
    crsCode=models.CharField(max_length=100)
    secId=models.PositiveIntegerField()
    semester=models.CharField(max_length=20)
    year=models.PositiveIntegerField()
    ploID=models.PositiveIntegerField()
    cloID=models.PositiveIntegerField()

class Teaches(models.Model):
    facultyId=models.PositiveIntegerField()
    crsCode=models.CharField(max_length=100)
    secId=models.PositiveIntegerField()
    semester=models.CharField(max_length=20)
    year=models.PositiveIntegerField()


class CLO(models.Model):
    cloId = models.CharField(max_length=10)
    cloName = models.CharField(max_length=10)

class PLO(models.Model):
    ploId = models.CharField(max_length=10)
    ploName = models.CharField(max_length=10)