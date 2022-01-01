from django.db import models
from django.contrib.auth import get_user_model
#from django.urls import reverse

# Create your models here.


class Activity(models.Model):
    activity_name = models.CharField(max_length=20, unique=True)
    activity_description = models.CharField(max_length=100)
    #location - add later
    
    def __str__(self):
        return f'Activity: {self.activity_name}'

class Student(models.Model):
    first_name = models.CharField(max_length=15, verbose_name="First Name")
    last_name = models.CharField(max_length=15, verbose_name="Last Name")
    student_email = models.EmailField(max_length=60)
    activities = models.ManyToManyField(Activity, through='Schedule')

    class Meta:
        unique_together = ['first_name', 'last_name']

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
   

class Schedule(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE) #PROTECT?
    session =  models.CharField(max_length=1)
    #add later
    #date_entered = models.DateField()

   


    
