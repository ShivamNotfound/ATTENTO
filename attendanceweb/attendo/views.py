from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
import json
from .models import Students,Classes,Faculty,StudentUser,Subject,Period,Attendance,AttendanceBuffer
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
import datetime
# Create your views here.

def home(request):
    return render(request,'home.html')


@ensure_csrf_cookie
def student_register(request):
    if request.method == 'POST':
        username=request.POST['username']
        password=request.POST['password']

        if StudentUser.objects.filter(username=username).exists():
            student_user=StudentUser.objects.get(username=username)

            if student_user.user:
                # already have an account
                return render(request,'student/student_register.html') 
            else:
                user=User.objects.create_user(username=username,password=password)
                user.save()
                student_user.user=user
                


        else:
            user=User.objects.create_user(username=username,password=password)
            user.save()
            StudentUser.objects.create(user=user,username=username)
        return redirect("/attendo/student/login")
    return render(request,'student/student_register.html')

@ensure_csrf_cookie
def student_login(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']

        user=authenticate(request,username=username,password=password)

        if user is not None:
            login(request,user)
            return redirect('/attendo/student/home')
    return render(request,'student/login.html')

def student_home(request):
    student=Students.objects.filter(username=request.user.username)
    
    return render(request,'student/home.html',{'student':student})

def subwise_attendance(request,class_id):
    student=Students.objects.get(username=request.user.username,classes_id=class_id)
    subjects=Subject.objects.filter(class_assigned_id=class_id)
    return render(request,'student/subwiseattend.html',{'student':student,'subjects':subjects,'class_id':class_id})
def subwise_history(request,class_id,sub_id):
    student=Students.objects.get(classes_id=class_id,username=request.user.username)
    attendance=Attendance.objects.filter(subject_id=sub_id,student_id=student.id)
    return render(request,'student/subattendhistory.html',{"attendance":attendance,'class_id':class_id})
def student_mark(request):
    students=Students.objects.filter(username=request.user.username)
    return render(request,'student/mark.html',{'students':students})

@ensure_csrf_cookie
def periodformarking(request,class_id):
    if request.method=="POST":
        status=request.POST['status']
        message=request.POST['reason']
        periods_chosen=request.POST.getlist('periods')
        student=Students.objects.get(username=request.user.username,classes_id=class_id)
        for period_id in periods_chosen:
            period=Period.objects.get(id=period_id)
            AttendanceBuffer.objects.create(status=status,date=datetime.date.today(),period=period.period,message=message,student_id=student.id,subject_id=period.subject_id)
        return redirect('/attendo/student/home')
    periods=Period.objects.filter(classes_id=class_id,day=datetime.date.today().strftime("%A").lower())

    return render(request,'student/markattenpersel.html',{'periods':periods})


def student_notification(request):
    return render(request,'student/notification.html')

def student_labexps(request):
    return render(request,'student/labExperiments.html')

def student_timetable(request):
    return render(request,'student/timeTable.html')

def student_history(request):
    return render(request,'student/history.html')

def student_calendar(request):
    return render(request,'student/calendar.html')

@ensure_csrf_cookie
def faculty_login(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']

        user=authenticate(request,username=username,password=password)

        if user is not None:
            login(request,user)
            return redirect('/attendo/faculty/home')
    return render(request,'faculty/login.html')
@ensure_csrf_cookie
def faculty_register(request):
    if request.method == 'POST':
        username=request.POST['username']
        password=request.POST['password']

        if Faculty.objects.filter(username=username).exists():
            faculty=Faculty.objects.get(username=username)

            if faculty.user:
                # already have an account
                return render(request,'faculty/register.html') 
            else:
                user=User.objects.create_user(username=username,password=password)
                user.save()
                faculty.user=user
                


        else:
            user=User.objects.create_user(username=username,password=password)
            user.save()
            Faculty.objects.create(user=user,username=username)
        return redirect("/attendo/faculty/login")
    return render(request,'faculty/register.html')

@ensure_csrf_cookie
def faculty_home(request):
    if request.method=='POST':
        data=json.loads(request.body)
        classes=Classes.objects.get(id=data['class_id'])
        classes.delete()
        return JsonResponse({
            'status':'success',
            'class_id':data['class_id']
        })
    faculty=Faculty.objects.get(username=request.user.username)
    classes=Classes.objects.filter(faculty=faculty)

    subject=Subject.objects.filter(username=request.user.username)
    return render(request,'Faculty/home.html',{'classes':classes,'subject':subject,'faculty':faculty})

def faculty_assigned(request):
    faculty=Faculty.objects.get(username=request.user.username)
    subjects=Subject.objects.filter(username=request.user.username)
    return render(request,'Faculty/assigned.html',{'faculty':faculty,'subjects':subjects})

def assigned_classes(request,class_id):
    periods=Period.objects.filter(classes_id=class_id,day=datetime.date.today().strftime("%A").lower())
    subject=Subject.objects.all()
    faculty=Faculty.objects.all()
    faculty_username=request.user.username
    return render(request,'Faculty/assignedlist.html',{'periods':periods,'subjects':subject,'faculty':faculty,'class_id':class_id,'faculty_name':faculty_username})

@ensure_csrf_cookie
def assigned_attendance(request,class_id,subject_id,period_num):
    if request.method=="POST":
        students=Students.objects.filter(classes_id=class_id)
        for student in students:
            status=request.POST[f"status{student.id}"]
            date=datetime.date.today()
            attendance=Attendance.objects.create(status=status,date=date,student_id=student.id,subject_id=subject_id,period=period_num)
        return redirect(f'/attendo/faculty/assignedclass')
    students=Students.objects.filter(classes_id=class_id)
    subject=Subject.objects.get(id=subject_id)
    return render(request,'Faculty/assignedattend.html',{'students':students,'subject':subject,'class_id':class_id,'period_num':period_num})


def faculty_history(request):
    return render(request,'Faculty/history.html')
@ensure_csrf_cookie
def faculty_studentlist(request,class_id):
    if request.method=="POST":
        data=json.loads(request.body)
        student=Students.objects.get(id=data['student_id'])
        student.delete()
        return JsonResponse(
            {'status':'success',
            }
        )
    classes=Classes.objects.get(id=class_id)
    students=Students.objects.filter(classes=class_id)
    return render(request,'Faculty/studentlist.html',{'students':students,'classes':classes})
@ensure_csrf_cookie
def faculty_addstu(request,class_id):
    if request.method=='POST':
        data=json.loads(request.body)
        if StudentUser.objects.filter(username=data['stu_username']).exists():
            student=Students.objects.create(
            name=data['name'],
            regno=data['regno'],
            classes_id=class_id,
            username=data['stu_username'],
            student_user_id=StudentUser.objects.get(username=data['stu_username']).id)
        else:
            student_user=StudentUser.objects.create(username=data['stu_username'])
            student=Students.objects.create(
                name=data['name'],
                username=data['stu_username'],
                regno=data['regno'],
                classes_id=class_id,
                student_user_id=student_user.id
        )
        return JsonResponse({
            'status':'success',
            'class_id':class_id
        })
    return render(request,"Faculty/addstu.html",{'class_id':class_id})


@ensure_csrf_cookie
def faculty_addclass(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        new_class = Classes.objects.create(
            degree  = data['degree'],
            branch  = data['branch'],
            section = data['section'],
            faculty=Faculty.objects.get(username=request.user.username)
        )

        return JsonResponse({
            'status'   : 'success',
            'class_id' : new_class.id
        })
    return render(request, 'Faculty/addclass.html')

def subjectview(request,class_id):
    subjects=Subject.objects.filter(class_assigned_id=class_id)
    return render(request,"faculty/subjectview.html",{'classes':class_id,'subjects':subjects})

@ensure_csrf_cookie
def add_sub(request,class_id):
    if request.method=='POST':
        name=request.POST['sub_name']
        username=request.POST['f_username']
        f_name=request.POST['f_name']
        if Faculty.objects.filter(username=username).exists():
            subject=Subject.objects.create(
            name=name,
            class_assigned_id=class_id,
            f_name=f_name,
            username=username,
            faculty_id=Faculty.objects.get(username=username).id)
        else:
            faculty=Faculty.objects.create(username=username)
            subject=Subject.objects.create(
                name=name,
                username=username,
                class_assigned_id=class_id,
                f_name=f_name,
                faculty_id=faculty.id
        )
        return redirect(f"/attendo/faculty/subjects/{class_id}")
    return render(request,"faculty/addsub.html",{'class_id':class_id})

@ensure_csrf_cookie
def faculty_timetable(request,class_id):      
    monday=Period.objects.filter(day='monday',classes_id=class_id)
    tuesday=Period.objects.filter(day='tuesday',classes_id=class_id)
    wednesday=Period.objects.filter(day='wednesday',classes_id=class_id)
    thursday=Period.objects.filter(day='thursday',classes_id=class_id)
    friday=Period.objects.filter(day='friday',classes_id=class_id)
    saturday=Period.objects.filter(day='saturday',classes_id=class_id)

    if request.method=='POST':
        day=request.POST.get('day')
        if day=='monday':
            monday.delete()
        elif day=='tuesday':
            tuesday.delete()
        elif day=='wednesday':
            wednesday.delete()
        elif day=='thursday':
            thursday.delete()
        elif day=='friday':
            friday.delete()
        else:
            saturday.delete()
    return render(request,"faculty/timetable.html",{'classes':class_id,'monday':monday,'tuesday':tuesday,'wednesday':wednesday,'thursday':thursday,'friday':friday,'saturday':saturday,'mon_len':len(monday),'tues_len':len(tuesday),'wed_len':len(wednesday),'thurs_len':len(thursday),'fri_len':len(friday),'sat_len':len(saturday)})

def faculty_addperiod(request,class_id,day,period_num):
    if request.method=='POST':
        s_name=request.POST['sub']
        s_time=(request.POST['s_time'].split(':'))
        e_time=request.POST['e_time'].split(":")
        subject=Subject.objects.get(class_assigned_id=class_id,name=s_name)
        period=Period.objects.create(
            start_time=datetime.time(int(s_time[0]),int(s_time[1])),
            end_time=datetime.time(int(e_time[0]),int(e_time[1])),
            classes_id=class_id,
            subject_id=subject.id,
            name=s_name,
            day=day,
            period=period_num
        )
        return redirect(f'/attendo/faculty/timetable/{class_id}')
    return render(request,'faculty/addperiod.html',{'class_id':class_id})
def faculty_chooseperiod(request,class_id):
    period=Period.objects.filter(classes_id=class_id,day=datetime.date.today().strftime("%A").lower())
    subject=Subject.objects.all()
    faculty=Faculty.objects.all()
    return render(request,'Faculty/chooseperiod.html',{'class_id':class_id,'periods':period,'subject':subject,'faculty':faculty})

@ensure_csrf_cookie
def mark_attendance(request,class_id,subject_id,period_num):
    if request.method=="POST":
        students=Students.objects.filter(classes_id=class_id)
        for student in students:
            status=request.POST[f"status{student.id}"]
            date=datetime.date.today()
            attendance=Attendance.objects.create(status=status,date=date,student_id=student.id,subject_id=subject_id,period=period_num)
        return redirect(f'/attendo/faculty/chooseperiod/{class_id}')
    students=Students.objects.filter(classes_id=class_id)
    subject=Subject.objects.get(id=subject_id)
    return render(request,'Faculty/markattendance.html',{'students':students,'subject':subject,'class_id':class_id,'period_num':period_num})


def logout_faculty(request):
    logout(request)
    return redirect("/attendo/home")