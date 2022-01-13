from django.test import TestCase
from django.urls import reverse
from django.test import RequestFactory


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
            'activity_name': 'Stand Up Paddleboard',
            'activity_description': 'SUP in the bay'
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
            'first_name': 'Joan',
            'last_name': 'Clarke',
            'student_email': 'jclarke@gmail.com'
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
        self.assertContains(response, 'Snorkel')
        self.assertContains(response, 'SUP')
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
        

class TestRunReport(TestCase):
    fixtures = ['test_students', 'test_activities', 'test_schedules' ]

    def test_run_report_shows_results(self):
        #report for students in session 1 and activity 2; should show 2 student; #1 and 2 
        response = self.client.post(reverse('run_report') , { 'activity': 2, 'session': 1})    
        # check redirect
        self.assertTemplateUsed('summer_fun/student_list.html')
        #TODO fix this test
        self.assertEqual(response.context['students'].count(), 2)
        #self.assertContains(response, 'Margaret') #student w/ pk2 is included
                #check results-#students with id2 and 1 are in the report; but not id3

        #self.assertEqual(2, len(response.context['students'])) #key error
        # students = list(response.context['students'].all())
        # self.assertEqual(2, len(students)) #key error: 'students'
        #self.assertEqual(2, response.context['students'].count())
      #  self.assertContains(response,'Margaret Hamilton')

    
    # def test_run_report_no_results(self):
    #     response = self.client.post(reverse('run_report') , { 'activity': 3, 'session': 1}) 
    #     self.assertContains(response, 'No students')