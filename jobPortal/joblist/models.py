from django.db import models
from django.utils import timezone
# Create your models here.

class Job(models.Model):
    job_title = models.CharField(max_length=100)
    company_name = models.CharField(max_length=100)
    job_description = models.TextField()
    job_location = models.CharField(max_length=100)
    job_type = models.CharField(max_length=20, choices=[
        ('fullTime', 'Full Time'),
        ('partTime', 'Part Time'),
        ('contract', 'Contract'),
        ('remote', 'Remote')
    ])
    job_postedby = models.CharField(max_length=100) 
    job_createdtime = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return self.job_title


class UserProfile(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    full_name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    resume = models.FileField(upload_to='resumes/')
    cover_letter = models.TextField()
    # Add more fields as needed, such as education, work experience, etc.
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username
    
class Recruiter(models.Model):
    username = models.CharField(max_length=150)
    password = models.CharField(max_length=128)
    email = models.EmailField()
    company_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20, blank=True, null=True)
    # Add more fields as needed, such as company size, industry, etc.

    def __str__(self):
        return self.username
    
class Application(models.Model):
    username = models.CharField(max_length=150)
    job = models.CharField(max_length=150)
    company_name = models.CharField(max_length=150,default="unknown")
    applied_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=150)

    def __str__(self):
        return self.username