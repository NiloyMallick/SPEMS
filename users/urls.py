from django.urls import path, include
from . import views

urlpatterns = [

    path('login/', views.Signin, name="signin"),
    path('logout/', views.Logout, name="logoutpage"),
    path('info/', views.StudentInfo, name="studentInfo"),
    path('plomap/', views.HigherAuth, name="ha"),
    path('faculty/', views.Faculties, name="faculties"),
    path('faculty/upload/', views.InfoUpload, name="uploaddetail"),
    path('faculty/upload/excel/', views.ExcelUpload, name ="uploadexcel"),


] 