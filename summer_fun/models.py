from django.db import models
from django.contrib.auth import get_user_model
#from django.urls import reverse

# Create your models here.


class Activity(models.Model):
    #in earlier version, had list of choices; now want
    #user to be able to add an activity (admin only eventually)
#     ACTIVITY_CHOICES = [
#     ('none', 'None'),
#     ('swim', 'Swim'),
#     ('hike', 'Hike'),
#     ('bike', 'Bike'),
#     ('kayak', 'Kayak'),
#     ('art', 'Art')

# ]
    activity_name = models.CharField(max_length=20)#, choices=ACTIVITY_CHOICES)
    activity_description = models.CharField(max_length=100)
    #location - add later
    
    def __str__(self):
        return f'Activity: {self.activity_name}'

class Student(models.Model):
    first_name = models.CharField(max_length=15, verbose_name="First Name")
    last_name = models.CharField(max_length=15, verbose_name="Last Name")
    student_email = models.EmailField(max_length=60)
    unique_together = ['first_name', 'last_name']
    activities = models.ManyToManyField(Activity, through='Schedule')

    def __str__(self):
        return f'Name: {self.first_name} {self.last_name}'
    
    # def get_absolute_url(self):
    #     return reverse('student-detail', kwargs={'pk':self.pk})

class Schedule(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE) #PROTECT?
    SESSIONS = (
        ('1', 'one'),
        ('2', 'two'),
        ('3', 'three'))

    #session_number = models.TextChoices('SessionNumber', '1 2 3 4')
    session = models.CharField(max_length=1, choices=SESSIONS)
    #add later
    #date_entered = models.DateField()



    
