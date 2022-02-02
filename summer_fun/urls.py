from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('student_list', views.student_list, name="student_list"),
    path('add_student', views.add_student, name='add_student'),
    path('student/<int:student_pk>/', views.student_details, name='student_details'),
  # path('student/<int:student_pk>/delete', views.delete_student, name='delete_student'),
    path('add_activity', views.add_activity, name='add_activity'),
    path('activity_list', views.activity_list, name='activity_list'),
    path('run_report', views.run_report, name='run_report'), 
    path('student/<int:student_pk>/edit', views.edit_schedule, name='edit_schedule'),
    path('activity/<int:activity_pk>/', views.activity_details, name='activity_details'),
    path('activity/<int:activity_pk>/delete', views.delete_activity, name='delete_activity')

]