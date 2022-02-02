from django.shortcuts import render, redirect, get_object_or_404
from .models import Student, Activity, Schedule
from .forms import NewStudentForm, SearchForm, ScheduleForm , NewActivityForm, ReportForm
from django.db.models.functions import Lower
from django.http import HttpResponseRedirect


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
            return redirect('student_list')
        else:
            #messages.warning(request, 'Check the data entered')
            return render(request, 'summer_fun/add_student.html', {'new_student_form': new_student_form })
    new_student_form = NewStudentForm
    return render(request, 'summer_fun/add_student.html', {'new_student_form': new_student_form })


def student_list(request):
    search_form = SearchForm(request.GET)
    if search_form.is_valid():
        search_term = search_form.cleaned_data['search_term']
        students = Student.objects.filter(first_name__icontains=search_term).order_by(Lower('first_name'))
        student_classes=get_student_classes(students) #call method below
    else: #show all students listin alpha order and the search form
        search_form = SearchForm()
        students = Student.objects.order_by(Lower('first_name'))
        student_classes = get_student_classes(students) 
    return render(request, 'summer_fun/student_list.html', { 'student_classes': student_classes, 'search_form': search_form})


def get_student_classes(students):
    student_classes ={}
    for student in students:
        this_students_classes =[]
        # all the activities and sessions belonging to this student
        c= list(Schedule.objects.filter(student = student))
        for x in c: #loop through schedule objects for this student
            activity = x.activity.activity_name #extract the activity name
            this_students_classes.append(activity) #add to listfor this student
        #dictionary[key]=value
        student_classes[student]=this_students_classes  
    return student_classes
    
        

def student_details(request, student_pk):
    student =  get_object_or_404(Student, pk=student_pk)
    if request.method == 'POST':
        schedule_form = ScheduleForm(request.POST)
        sessions = 3 #make it a global var??
        activityData = request.POST.getlist('activity')  #this list is indexed 0,1,2  
      #  for instance in range(0, sessions-1):     
        for instance in range(0, sessions):    
            activity = get_object_or_404(Activity, pk=activityData[instance])
            #create and save a new Schedule object
            createObj = Schedule.objects.create(
                student = student,
                session = instance+1,
                activity = activity
            ) 
            createObj.save()
        return redirect('student_list')
    else:
        #get info from dbase on this student's classes
        student_classes = Schedule.objects.filter(student = student)
        if student_classes: # if schedule already in dbase
            return render(request, 'summer_fun/student_details.html', { 'student': student, 'student_classes': student_classes})
        else:  #display the blank form  
            schedule_form = ScheduleForm
            return render(request, 'summer_fun/student_details.html', { 'student': student, 'schedule_form': schedule_form, "sessions": range(1,4)})

def activity_details(request, activity_pk):
    activity =  get_object_or_404(Activity, pk=activity_pk)
    return render(request, 'summer_fun/activity_details.html', {'activity': activity})





def edit_schedule(request, student_pk):
    student =  get_object_or_404(Student, pk=student_pk) 
    student_classes = Schedule.objects.filter(student = student) #a query set of schedule objects
    if request.method == 'GET':
        schedule_form = ScheduleForm
        return render(request, 'summer_fun/edit_schedule.html', {'student': student,'schedule_form': schedule_form, 'student_classes': student_classes, "sessions": range(1,4)}) 
    else: #request is POST
        schedule_form = ScheduleForm(request.POST)
        if schedule_form.is_valid():
            activityData = request.POST.getlist('activity') 
            #retrieve schedule objects for this student
            student_classes = Schedule.objects.filter(student = student)
            #modify them with new activity choices
            i=0
            for s in student_classes:
                activity = get_object_or_404(Activity, pk=activityData[i])
                s.activity = activity #update this schedfule's activity
                s.save() #save the new schedule object
                i+=1
            #messages.info(request, 'Edit saved')
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

def delete_activity(request, activity_pk):
    activity = get_object_or_404(Activity, pk=activity_pk)
    activity.delete()
    return redirect('activity_list')


def run_report(request):
    if request.method =='POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            activity_term = form.cleaned_data['activity_name']
            act_id = Activity.objects.get(activity_name = activity_term)
            session_num = form.cleaned_data['session_num']
            #may need name__iexact=to get case insensitive matches
            students = Schedule.objects.filter(activity=act_id,session= session_num)
            return render(request, 'summer_fun/report_results.html', {'students': students, 'activity': activity_term , 'session': session_num})
    else: #GET - just show the form
        form = ReportForm()
    return render(request, 'summer_fun/run_report.html', {'form': form})

