from django.urls import path
from . import views


urlpatterns=[path("student/home",views.student_home,name="student_interface"),
             path("student/mark",views.student_mark,name="student_mark"),
             path("student/mark/periods/<int:class_id>/",views.periodformarking,name="periodformarking"),
             path("student/notification",views.student_notification,name="student_notification"),
             path("student/labExperiments",views.student_labexps,name="student_labexps"),
             path("student/timeTable",views.student_timetable,name="student_timetable"),
             path("student/history",views.student_history,name="student_history"),
             path("student/calendar",views.student_calendar,name="student_calendar"),
             path("faculty/home",views.faculty_home,name="faculty_interface"),
             path("faculty/assignedclass",views.faculty_assigned,name="faculty_assigned"),
             path("faculty/history",views.faculty_history,name="faculty_history"),
            path('faculty/addclass/', views.faculty_addclass, name='faculty_addclass'),
            path('faculty/studentlist/<int:class_id>/', views.faculty_studentlist, name='faculty_studentlist'),
            path('faculty/studentlist/<int:class_id>/addstu', views.faculty_addstu, name='faculty_addstu'),
            path('faculty/register', views.faculty_register, name='faculty_register'),
            path('faculty/login', views.faculty_login, name='faculty_login'),
            path('student/register', views.student_register, name='student_register'),
            path('student/login', views.student_login, name='student_login'),
            path('faculty/subjects/<int:class_id>/', views.subjectview, name='subjectview'),
            path('faculty/subjects/<int:class_id>/addsub/', views.add_sub, name='addsub'),
            path('faculty/timetable/<int:class_id>/',views.faculty_timetable,name='faculty_timetable'),
            path('faculty/timetable/<int:class_id>/addperiod/<str:day>/<int:period_num>',views.faculty_addperiod,name='faculty_addperiod'),
            path('faculty/chooseperiod/<int:class_id>',views.faculty_chooseperiod,name='faculty_chooseperiod'),
            path('faculty/markattendance/<int:class_id>/<int:subject_id>/<int:period_num>',views.mark_attendance,name='mark_attendance'),
            path('faculty/assigned_classes/<int:class_id>',views.assigned_classes,name='assigned_classes'),
            path('faculty/assigned/markattendance/<int:class_id>/<int:subject_id>/<int:period_num>',views.assigned_attendance,name='assigned_attendance'),
            path('faculty/logout',views.logout_faculty,name='logout'),
            path('home',views.home,name='home'),
            path('student/subwiseAttendance/<int:class_id>',views.subwise_attendance,name='subwise_attendance'),
            path('student/subwiseAttendance/<int:class_id>/subwisehistory/<int:sub_id>',views.subwise_history,name='subwise_history')
]           
             
             