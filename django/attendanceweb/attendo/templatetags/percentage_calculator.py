from django import template
from attendo.models import Attendance,AttendanceBuffer
import datetime

register=template.Library()

@register.simple_tag
def percalculate(stu_id):
    try:
        total_attendance=Attendance.objects.filter(student_id=stu_id)
        present=Attendance.objects.filter(student_id=stu_id).exclude(status='absent')
        attendance_percentage=len(present)/len(total_attendance) * 100
        return int(attendance_percentage)
    except Exception:
        return None 
    
@register.simple_tag
def subwise_percentage(stu_id,sub_id):
    try:
        total_attendance=Attendance.objects.filter(student_id=stu_id,subject_id=sub_id)
        present=Attendance.objects.filter(student_id=stu_id,subject_id=sub_id).exclude(status='absent')
        attendance_percentage=len(present)/len(total_attendance) * 100
        return int(attendance_percentage)
    except Exception:
        return None
    
@register.simple_tag
def check_period_dup(period,sub_id):
    attend=Attendance.objects.filter(date=datetime.date.today(),period=period,subject_id=sub_id)
    if attend.exists():
        return False
    else:
        return True
    
@register.simple_tag
def check_marked(student_id,subject_id,period_num):
    buffer=AttendanceBuffer.objects.filter(student_id=student_id,subject_id=subject_id,period=period_num,date=datetime.date.today())
    if buffer.exists():
        return AttendanceBuffer.objects.get(student_id=student_id,subject_id=subject_id,period=period_num,date=datetime.date.today())
    return None