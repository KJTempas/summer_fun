from django.shortcuts import render, redirect, get_object_or_404
from .models import Student, Activity, Schedule
from .forms import NewStudentForm, SearchForm, ScheduleForm , NewActivityForm
from django.db.models.functions import Lower

# Create your views here.
def home(request):
    app_name = 'Summer Fun Signup'
    return render(request, 'summer_fun/home.html', {'app_name': app_name})

def add_student(request):
    if request.method == 'POST':
        #create a form instance from POST data
        new_student_form = NewStudentForm(request.POST)#, instance= Student())
        if new_student_form.is_valid():
            new_student_form.save()
        #save new Student object from form's data
            #student = student_form.save()
            return redirect('student_list')
        #return render(request, 'summer_fun/select_classes.html', {'select_form': select_form})
        else:
            #messages.warning(request, 'Check the data entered')
            return render(request, 'summer_fun/add_student.html', {'new_student_form': new_student_form })
    new_student_form = NewStudentForm
    return render(request, 'summer_fun/add_student.html', {'new_student_form': new_student_form })


def student_list(request):
    search_form = SearchForm(request.GET)
    if search_form.is_valid():
        search_term = search_form.cleaned_data['search_term']
        students = Student.objects.filter(first_name__icontains=search_term).order_by('first_name')
    else:
        search_form = SearchForm()
        students = Student.objects.order_by(Lower('first_name'))
    return render(request, 'summer_fun/student_list.html', {'students': students, 'search_form':search_form })

def student_details(request, student_pk):
    student = get_object_or_404(Student, pk=student_pk)
    return render(request, 'summer_fun/student_details.html', {'student': student})

def add_classes(request, student_pk):
    if request.method == 'POST':
        form = ScheduleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('student_details')
        else:
            return render(request, 'summer_fun/add_classes.html', { 'form': form, })
    form = ScheduleForm
    return render(request, 'summer_fun/student_details.html', {'form': form })

def delete_student(request, student_pk):
    student = get_object_or_404(Student, pk=student_pk)
    student.delete()
    return redirect('student_list')

def add_activity(request):
    if request.method == 'POST':
        #create a form instance from POST data
        new_activity_form = NewActivityForm(request.POST)#, instance= Student())
        if new_activity_form.is_valid():
            new_activity_form.save()
        #save new Activity object from form's data
            return redirect('activity_list')
        else:
            #messages.warning(request, 'Check the data entered')
            return render(request, 'summer_fun/add_activity.html', {'new_activity_form': new_activity_form })
    new_activity_form = NewActivityForm
    return render(request, 'summer_fun/add_activity.html', {'new_activity_form': new_activity_form })


def activity_list(request):
    search_form = SearchForm(request.GET)
    if search_form.is_valid():
        search_term = search_form.cleaned_data['search_term']
        activities = Activity.objects.filter(activity_name__icontains=search_term)
    else:
        search_form = SearchForm()
        activities = Activity.objects.all()
    return render(request, 'summer_fun/activity_list.html', {'activities': activities, 'search_form':search_form })


