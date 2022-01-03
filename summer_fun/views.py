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
        #return render(request, 'summer_fun/select_classes.html', {'select_form': select_form})
        else:
            #messages.warning(request, 'Check the data entered')
            return render(request, 'summer_fun/add_student.html', {'new_student_form': new_student_form })
    new_student_form = NewStudentForm
    return render(request, 'summer_fun/add_student.html', {'new_student_form': new_student_form })


def student_list(request):
    students = Student.objects.order_by(Lower('first_name'))
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
        
    return render(request, 'summer_fun/student_list.html', { 'student_classes': student_classes})
       

def student_details(request, student_pk):
    student =  get_object_or_404(Student, pk=student_pk)
    if request.method == 'POST':
        schedule_form = ScheduleForm(request.POST)
        sessions = 3 #make it a global var??
        activityData = request.POST.getlist('activity')    
        for instance in range(0, sessions-1):       
            activity = get_object_or_404(Activity, pk=activityData[instance])
            #create and save a new Schedule object
            createObj = Schedule.objects.create(
                student = student,
                session = instance+1,
                activity = activity
            ) 
            createObj.save()
        return redirect('student_list')
    else: #a GET
        #get info from dbase on this student's classes
        student_classes = Schedule.objects.filter(student = student)
        if student_classes: # if schedule already in dbase
            return render(request, 'summer_fun/student_details.html', { 'student': student, 'student_classes': student_classes})# "sessions": range(1,3)})
        else:  #display the blank form  
            schedule_form = ScheduleForm
            return render(request, 'summer_fun/student_details.html', { 'student': student, 'schedule_form': schedule_form, "sessions": range(1,3)})
        

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


#TODO fix display and saving of classes
def select_classes(request, student_pk):
    student =  get_object_or_404(Student, pk=student_pk)
    print('hello')
    if request.method == 'POST':
        print('you are here 1')
        schedule_form = ScheduleForm(request.POST)
        sessions = 3 #make it a global var??
        activityData = request.POST.getlist('activity')    
        for instance in range(0, sessions-1):       
            activity = get_object_or_404(Activity, pk=activityData[instance])
            print(activity.activity_name)
            #create and save a new Schedule object
            createObj = Schedule.objects.create(
                student = student,
                session = instance+1,
                activity = activity
            ) 
            createObj.save()
        return redirect('student_list')

    else: #GET
        print('you are here 2')
        #should be multiple schedule objects for this student
        #TODO work here to get current schedule to display
        #get a queryset of schedule objects for this student
        student_classes = Schedule.objects.filter(student = student) 
        #schedule_form = ScheduleForm(instance=schedules) 
        #send to new template; add Edit to this template
        return render(request, 'summer_fun/student_details.html', { 'student': student, 'student_classes': student_classes})# "sessions": range(1,3)})
     #display the blank form       
    schedule_form = ScheduleForm
    print('you are here 3')
    return render(request, 'summer_fun/select_classes.html', {'schedule_form': schedule_form, 'student': student, "sessions": range(1,3)})




def run_report(request):
    if request.method =='POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            activity_term = form.cleaned_data['activity_name']
            act_id = Activity.objects.get(activity_name = activity_term)
            session_num = form.cleaned_data['session_num']
            #may need name__iexact=to get case insensitive matches
            students = Schedule.objects.filter(activity=act_id,session= session_num)
    #TODO fix session numbersfrom 0 and 1 to 1 and 2
            return render(request, 'summer_fun/report_results.html', {'students': students, 'activity': activity_term , 'session': session_num})
    else: #GET - just show the form
        form = ReportForm()
    return render(request, 'summer_fun/run_report.html', {'form': form})
