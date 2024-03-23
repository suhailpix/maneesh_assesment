from django.contrib import admin
from .models import Job,UserProfile,Recruiter,Application

admin.site.register(Job)  # Register your Job model
admin.site.register(UserProfile)  # Register your UserProfile model
admin.site.register(Recruiter)  # Register your Recruiter model
admin.site.register(Application)  # Register your Application model