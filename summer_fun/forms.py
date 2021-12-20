from django import forms
from django.forms import ModelForm
from .models import Student, Activity, Schedule

#http://www.learningaboutelectronics.com/Articles/How-to-create-a-drop-down-list-in-a-Django-form.php
#https://www.geeksforgeeks.org/how-to-use-django-field-choices/

class NewStudentForm(ModelForm):
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'student_email']

class SearchForm(forms.Form):
    search_term = forms.CharField()

class NewActivityForm(ModelForm):
    class Meta:
        model = Activity
        fields = ['activity_name', 'activity_description']

class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = [ 'activity']
    #could use exclude

#current form is like search form;laterversion could have drop down
# of activity.activity_name as a picklist
class ReportForm(forms.Form):
    activity_name = forms.CharField(label='activity name')
    session_num = forms.IntegerField(label='session number')
