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
        