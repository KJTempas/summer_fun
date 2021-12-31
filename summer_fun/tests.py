from django.test import TestCase
from django.urls import reverse

from summer_fun.models import Activity

# Create your tests here.
#to run these tests, in summerfun, type python manage.py test

class TestViewActivitiesPage(TestCase):

    fixtures = ['test_activities'] #fixtures has 3 activites

    def test_load_activity_list_shows_three_activities(self):
        response = self.client.get(reverse('activity_list'))
        self.assertTemplateUsed(response, 'summer_fun/activity_list.html')
        self.assertEquals(3, len(response.context['activities'])) 



class TestAddActivities(TestCase):

    #fixtures = ['test_activities']

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
        activity_one = Activity.objects.first()
        #check its properties
        self.assertEqual('Snorkeling', activity_one.activity_name)