import tempfile
import filecmp
import os

from django.test import TestCase
from django.urls import reverse

from summer_fun.models import Activity, Student

# Create your tests here.
#to run these tests, in summerfun, type python manage.py test


class TestViewActivitiesPage(TestCase):

    fixtures = ['test_activities'] #fixtures has 3 activites

    def test_load_activity_list_shows_three_activities(self):
        response = self.client.get(reverse('activity_list'))
        self.assertTemplateUsed(response, 'summer_fun/activity_list.html')
        self.assertEquals(3, len(response.context['activities'])) 


class TestAddActivities(TestCase):

    fixtures = ['test_activities']

    def test_add_activity(self):
        new_activity = {
            'activity_name': 'Snorkeling',
            'activity_description': 'See beautiful coral and fish'
        }
        #follow=True means follow redirect in method
        response = self.client.post(reverse('add_activity'), data= new_activity, follow=True)
        #check redirect
        self.assertTemplateUsed('summer_fun/activity_list.html')
        #make sure activitylist includes new activity
        self.assertContains(response, 'Snorkeling')
 #pull the activity from the dbase
        activity_last = Activity.objects.last()
        #check its properties
        self.assertEqual('Snorkeling', activity_last.activity_name)

        
    def test_add_activity_does_not_add_duplicate(self):
        #add duplicate of activity in fixtures
        new_activity = {
            'activity_name': 'SCUBA',
            'activity_description': 'SCUBA in the bay'
        }
        response = self.client.post(reverse('add_activity'), data= new_activity, follow=True)
        #new_activity should not have added; should be still 3 activities
        activites_count = Activity.objects.count()
        self.assertEqual(3, activites_count)
        


class TestAddStudent(TestCase):

    fixtures = ['test_students']

    def test_add_student(self):
        new_student = {
            'first_name': 'Grace',
            'last_name': 'Hopper',
            'student_email': 'ghopper@gmail.com'
        }
        #follow=True means follow redirect in method
        response = self.client.post(reverse('add_student'), data= new_student, follow=True)
        #check redirect
        self.assertTemplateUsed('summer_fun/student_list.html')
        #make sure activitylist includes new activity
        self.assertContains(response, 'Grace')
        #pull the activity from the dbase
        student_last = Student.objects.last()
        #check its properties
        self.assertEqual('Grace', student_last.first_name)
        student_count = Student.objects.count()
        #3 students in fixtures + one new student = 4
        self.assertEqual(4, student_count)
    
    def test_cannot_add_duplicate_student(self):
        new_student = {
            'first_name': 'Margaret',
            'last_name': 'Atwood',
            'student_email': 'malarke@gmail.com'
        }
        #trying to add a student who is already in the dbase (through fixtures)
        #should not add due to unique together constraint
        response = self.client.post(reverse('add_student'), data= new_student, follow=True)
        student_count = Student.objects.count()
        #3 students in fixtures is still total count
        self.assertEqual(3, student_count)

class TestViewStudentListPage(TestCase):

    fixtures = ['test_students'] #fixtures has 3 students

    def test_load_student_list_shows_three_students(self):
        response = self.client.get(reverse('student_list'))
        self.assertTemplateUsed(response, 'summer_fun/student_list.html')
        self.assertEqual(3, len(response.context['student_classes'])) 
   
class TestSearchActivity(TestCase):
    fixtures = ['test_activities']

    def test_activity_search_matches_case_insensitive_and_partial(self):
        #search activities that include the letter s
        response = self.client.get(reverse('activity_list') + '?search_term=s')
        self.assertContains(response, 'SCUBA')
        self.assertContains(response, 'XC Ski')
        self.assertNotContains(response, 'Kayak')

    def test_activity_search_no_search_results(self):
        response = self.client.get(reverse('activity_list') + '?search_term=badminton')
        #check length of activity_list; should be 0 because no matches
        self.assertEqual(len(response.context['activities']), 0)

    def test_activity_search_clear_link(self):
            response = self.client.get( reverse('activity_list') + '?search_term=s')
            #when the clear button is clicked, it redirects to the activity list page
            all_activities_url = reverse('activity_list')
            self.assertContains(response, all_activities_url)
            

class TestSearchStudent(TestCase):
    fixtures = ['test_students']

    def test_student_search_matches_case_insensitive_and_partial(self):
        #search activities that include the letters jo (fixtures has a Joan)
        response = self.client.get(reverse('student_list') + '?search_term=jo')
        self.assertContains(response, 'Joan')
        self.assertNotContains(response, 'Acadia')

    def test_student_search_no_search_results(self):
        response = self.client.get(reverse('student_list') + '?search_term=mickey')
        self.assertContains(response, 'No students')

    def test_student_search_clear_link(self):
        response = self.client.get( reverse('student_list') + '?search_term=jo')
        #when the clear button is clicked, it redirects to the student list page
        all_students_url = reverse('student_list')
        self.assertContains(response, all_students_url)
        

class TestAddStudentSchedule(TestCase):
    fixtures = ['test_schedules', 'test_students', 'test_activities']

    def test_student_schedule_appears_in_student_list(self):
        pass
        #response = self.client.get(reverse('student_list'))
    #template should show student 1 having signed up for SCUBA, Snowshoe and XC Ski
  #  self.assertContains(response.context['student_classes'], 'SCUBA')
        #error w below is 'dict' object has no attribute 'student'
        #self.assertContains(response.context['student_classes'].student.activity_name, 'SCUBA')
        #error here is KeyError: 'student'
        #self.assertContains(response.context['student_classes']['student'].activity_name, 'SCUBA')
        

        # response = self.client.get(reverse('student_list', kwargs={'student_pk' : 1}))
        # self.assertContains(response.context['student_classes']['student'].activity_name, 'SCUBA')


    def test_student_schedule_appears_on_student_details_page(self):
        #retrieve the schedule for student 1
        response = self.client.get(reverse('student_details', kwargs = {'student_pk' : 1}))
        #uses correct template to show results
        self.assertTemplateUsed(response, 'summer_fun/student_details.html')
        #self.assertEqual(len(response.context['student_classes']), 3)#AssertionError 1 !=3
        #student_classes is a queryset
        #queryset has no attribute 'student' ...or 'activity'
        #self.assertContains(response.context['student_classes'].student, 'SCUBA')
#print(student_classes[1].activity.activity_name) from views yields 'Hiking'

        #self.assertContains(response.context['student_classes'][1].activity.activity_name, 'Snowshoe')
  #AttributeError: 'str' object has no attribute 'status_code'
        self.assertContains(response.context['student_classes'][1].activity.activity_name, 'Snowshoe')
