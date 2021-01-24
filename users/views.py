from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from django.http import JsonResponse
from .models import Student, Faculty, Department, Course, Takes, Section, Teaches
import openpyxl


# Create your views here.


def Home(request):
    if not request.user.is_authenticated:
        return render(request, 'users/signinpage.html',{'name': 'Sign in'})
    else:
        uId = request.user.username
        numberOfStudent = Takes.objects.values('stdId').distinct().count
        numberOfCourse = Course.objects.count()
        numberOfFaculty = Faculty.objects.count()
        numberOfPlo = Section.objects.values('ploID').distinct().count()
        numberOfSemester = Section.objects.values('semester').distinct().count()
        avgPloMap = numberOfCourse/numberOfPlo
        avgSemester = numberOfSemester/numberOfFaculty
        return render(request, 'users/homepage.html', {'name': 'Home page', 'uId': uId, 'numberOfStudent':numberOfStudent, 'numberOfCourse':numberOfCourse, 'numberOfFaculty': numberOfFaculty, 'numberOfPlo':numberOfPlo, 'avgPloMap':avgPloMap, 'avgSemester':avgSemester})


def Signin(request):
    if request.method == 'POST':
        user = auth.authenticate(username = request.POST['username'], password = request.POST['userPassword'])
        if user is not None:
            auth.login(request, user)
            return redirect("homepage")
        else:
            return render(request, 'users/signinpage.html',{'name': 'Sign in', 'error':"Your user name and password don't match"})
    else:
        return render(request, 'users/signinpage.html',{'name': 'Sign in'})


def Logout(request):
    if request.method == "POST":
        auth.logout(request)
        return redirect('signin')

def plo_chart1(request):
    if not request.user.is_authenticated:
        return render(request, 'users/signinpage.html',{'name': 'Sign in','error':'Please login first!'})
    else:
        studentID = request.user.username
        stdInfo = Student.objects.get(stdId=studentID)
        stdCourse = Takes.objects.filter(stdId = studentID)

        data = ['16.34', '44.84', '74.34', '34.43', '16.34', '44.84', '74.34', '34.43', '48.34', '73.84']
        labels = ['PLO01', 'PLO02', 'PLO03', 'PLO04', 'PLO05', 'PLO06', 'PLO07', 'PLO08', 'PLO09', 'PLO10', 'PLO11', 'PLO12' ]
        for i in range(len(labels)):
            incr = 1
            sum = 0.0
            for val in stdCourse:
                 if val.ploID == i: 
                    sum = sum + float(val.marks)
                    incr = incr + 1
            if(incr>1):
                val = sum/(incr-1)
                data.append(val)
            else:
                data.append(sum)
    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })

def StudentInfo(request):
    if not request.user.is_authenticated:
        return render(request, 'users/signinpage.html',{'name': 'Sign in','error':'Please login first!'})
    else:
        studentID = request.user.username
        stdInfo = Student.objects.get(stdId=studentID)
        return render(request, 'users/studentinfo.html',{'name': 'Student Info', 'stdId': studentID, 'stdInfo' : stdInfo })

def HigherAuth(request):
    if not request.user.is_authenticated:
        return render(request, 'users/signinpage.html',{'name': 'Sign in','error':'Please login first!'})
    else:
        if request.method == 'POST':
            courseDetailsNumber = Section.objects.filter(crsCode = request.POST['courseId'], secId = request.POST['secId'], semester = request.POST['semester'], year = request.POST['year'], ploID = request.POST['ploId'], cloID = request.POST['cloId']).count()
            if courseDetailsNumber >= 1:    
                return render(request, 'users/plomapping.html', {'name': 'Higher Authority', 'error': 'Already exists!'})
            else:
                courseDetails = Section(crsCode = request.POST['courseId'], secId = request.POST['secId'], semester = request.POST['semester'], year = request.POST['year'], ploID = request.POST['ploId'], cloID = request.POST['cloId'])
                courseDetails.save()
                return render(request, 'users/plomapping.html', {'name': 'Higher Authority', 'notification': 'Successfully update!'})
        else:
            return render(request, 'users/plomapping.html', {'name': 'Higher Authority'})

def Faculties(request):
    if not request.user.is_authenticated:
        return render(request, 'users/signinpage.html',{'name': 'Sign in','error':'Please login first!'})
    else:
        if request.method == 'POST':
            l11 = 0
            l22 = 0
            l1 = Takes.objects.filter(crsCode = request.POST['courseId'], secId = request.POST['secId'], semester = request.POST['semester'], year = request.POST['year']).count()
            l2 = Section.objects.filter(crsCode = request.POST['courseId'], secId = request.POST['secId'], semester = request.POST['semester'], year = request.POST['year']).count()
            studentDetailsObject = Takes.objects.filter(crsCode = request.POST['courseId'], secId = request.POST['secId'], semester = request.POST['semester'], year = request.POST['year'])
            PLOCLODetails = Section.objects.filter(crsCode = request.POST['courseId'], secId = request.POST['secId'], semester = request.POST['semester'], year = request.POST['year'])
            return render(request, 'users/fac1.html',{'name': 'Details page', 'l1': l1, 'l2':l2, 'l11': l11, 'l22':l22, 'studentDetailsObject': studentDetailsObject, 'PLOCLODetails': PLOCLODetails})
        else:
            return render(request, 'users/resultupload.html')


def InfoUpload(request):
    if not request.user.is_authenticated:
        return render(request, 'users/signinpage.html',{'name': 'Sign in','error':'Please login first!'})
    else:
        if request.method == 'POST':
            takesDetailsNumber = Takes.objects.filter(crsCode = request.POST['courseId'], secId = request.POST['secId'], semester = request.POST['semester'], year = request.POST['year'], stdId = request.POST['stdId'], ploID = request.POST['ploId'], cloID = request.POST['cloId']).count()
            if takesDetailsNumber >= 1:    
                return render(request, 'users/uploaddetail.html', { 'error': 'Already uploaded!'})
            else:
                takesDetails = Takes(crsCode = request.POST['courseId'], secId = request.POST['secId'], semester = request.POST['semester'], year = request.POST['year'], stdId = request.POST['stdId'], marks = request.POST['marks'], ploID = request.POST['ploId'], cloID = request.POST['cloId'])
                takesDetails.save()
                return render(request, 'users/uploaddetail.html', { 'notification': 'Successfully upload!'})
        else:
            return render(request, 'users/uploaddetail.html')

def ExcelUpload(request):
    if not request.user.is_authenticated:
        return render(request, 'users/signinpage.html',{'name': 'Sign in','error':'Please login first!'})
    else:
        if request.method == 'POST':           
            excel_file = request.FILES["excel_file"]
        
        # you may put validations here to check extension or file size

            wb = openpyxl.load_workbook(excel_file)

        # getting a particular sheet by name out of many sheets
            worksheet = wb["Sheet1"]
            print(worksheet)

            excel_data = list()
        # iterating over the rows and
        # getting value from each cell in row
            for row in worksheet.iter_rows():
                row_data = list()
                for cell in row:
                    row_data.append(str(cell.value))
                excel_data.append(row_data)
            return render(request, 'users/uploaddetail.html', {"excel_data":excel_data, 'notification': 'Successfully upload!'})
        else:
            return render(request, 'users/uploaddetail.html')