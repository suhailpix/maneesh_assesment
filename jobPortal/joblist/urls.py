from django.contrib import admin
from django.urls import path,include
from joblist.views import *

urlpatterns = [
    path('', login_view, name='login'),
    path('home',home,name="home" ),
    path('logout/', logout_view, name='logout'),
    path('addJob/',addJob,name="addJob" ),
    path('signup_select/', signup_select, name='signup_select'),
    path('signup/', signup_view, name='signup'),
    path('signup_recruiter/', signup_recruiter, name='signup_recruiter'),
    path('profile/', profile, name='profile'),
    path('apply_for_job/', apply_for_job, name='apply_for_job'),
    path('track_applications/', track_applications, name='track_applications'),
    path('all_applicants/', all_applicants, name='all_applicants'),
    path('update_application_status/', update_application_status, name='update_application_status'),
]