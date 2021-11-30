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

class ScheduleForm(ModelForm):
    class Meta:
        model = Schedule
        fields = ['session', 'activity']
# class ScheduleForm(forms.Form):
#     session =forms.ChoiceField()

# def generateView(request):
#     if request.method == 'POST':
#         student_form = StudentForm(request.POST, prefix = "student")
#         activity_form = ActivityForm(request.POST, prefix = "a")
#         schedule_form = ScheduleForm(request.POST, prefix = "sch")
#         if StudentForm.is_valid() and ActivityForm.is_valid() and ScheduleForm.is_valid():
#            # print "all valdcation passed"
#             student = student_form.save()
#             activity_form.cleaned_data["student"]