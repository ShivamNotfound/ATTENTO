from django.db import models
from django.contrib.auth.models import User
# Create your models here.


    

class Faculty(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,null=True)
    username=models.CharField(max_length=30,null=True)
class StudentUser(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,null=True)
    username=models.CharField(max_length=30,null=True)

class Classes(models.Model):
    degree=models.CharField(max_length=20)
    branch=models.CharField(max_length=20)
    section=models.CharField(max_length=10)
    faculty=models.ForeignKey(Faculty,on_delete=models.CASCADE,null=True,blank=True)


    def __str__(self):
        return f"{self.degree}({self.branch}-{self.section})"

class Subject(models.Model):
    name=models.CharField(max_length=30)
    class_assigned=models.ForeignKey(Classes,on_delete=models.CASCADE)
    f_name=models.CharField(max_length=30,null=True)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    username=models.CharField(max_length=30,null=True)
class Students(models.Model):
    student_user=models.ForeignKey(StudentUser,on_delete=models.CASCADE,null=True)
    name=models.CharField(max_length=30)
    username=models.CharField(max_length=30,null=True)
    regno=models.CharField(max_length=35)
    classes=models.ForeignKey(Classes,on_delete=models.CASCADE)
class Attendance(models.Model):
    student=models.ForeignKey(Students,on_delete=models.CASCADE,null=True)
    status=models.CharField(max_length=20)
    date=models.DateField(max_length=20)
    subject=models.ForeignKey(Subject,on_delete=models.CASCADE,null=True)
    period=models.CharField(max_length=10,null=True)
class Period(models.Model):
    name=models.CharField(max_length=30,null=True)
    subject=models.ForeignKey(Subject,on_delete=models.CASCADE,null=True)
    classes=models.ForeignKey(Classes,on_delete=models.CASCADE,null=True)
    day=models.CharField(max_length=24)
    start_time=models.TimeField(null=True)
    end_time=models.TimeField(null=True)
    period=models.CharField(max_length=10,null=True)
class AttendanceBuffer(models.Model):
    student=models.ForeignKey(Students,on_delete=models.CASCADE,null=True)
    status=models.CharField(max_length=20)
    date=models.DateField(max_length=20)
    subject=models.ForeignKey(Subject,on_delete=models.CASCADE,null=True)
    period=models.CharField(max_length=10,null=True)
    message=models.CharField(max_length=100,null=True)

    



    
