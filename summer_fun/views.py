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
        for student in students:
            print(student.first_name)
            #should yield all the activities and sessions belonging to this student
            classes= Schedule.objects.filter(student = student)
            print(classes) #aqueryset
            for x in classes:
                print(x.session) #prints 0 or 1...
                print(x.activity) #prints SUP or Swimming...
                
        return render(request, 'summer_fun/student_list.html', {'students': students, 'search_form':search_form ,'classes': classes})

    return render(request, 'summer_fun/student_list.html', {'students': students, 'search_form':search_form , 'classes': classes})

#TODO eventually
# def student_details(request, student_pk):
#     student = get_object_or_404(Student, pk=student_pk)
#     print(student.first_name) #printing
#     return render(request, 'summer_fun/student_details.html', {'student': student})
    

def select_classes(request, student_pk):
    student =  get_object_or_404(Student, pk=student_pk)
    
    if request.method == 'POST':
        schedule_form = ScheduleForm(request.POST)
        sessions = 3
        activityData = request.POST.getlist('activity')
        for instance in range(sessions-1):
            activity = get_object_or_404(Activity, pk=activityData[instance])
        
            createObj = Schedule.objects.create(
                student = student,
                session = instance,
                activity = activity
            )
            createObj.save()
        return redirect('student_list')

    else: #GET
        schedule_form = ScheduleForm()
        return render(request, 'summer_fun/select_classes.html', {'schedule_form': schedule_form, 'student': student, "sessions": range(1,3)})
            
    schedule_form = ScheduleForm
    return render(request, 'summer_fun/select_classes.html', {'schedule_form': schedule_form, 'student': student, "sessions": range(1,3)})


# def delete_student(request, student_pk):
#     student = get_object_or_404(Student, pk=student_pk)
#     student.delete()
#     return redirect('student_list')

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
    #GET request
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


