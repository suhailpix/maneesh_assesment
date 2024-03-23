from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required 
from .models import Job,UserProfile,Recruiter,Application
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.http import JsonResponse
from django.contrib.auth import login, logout

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = UserProfile.objects.filter(username=username, password=password).first()
        if user is not None:
            request.session['loginusername'] = username
            request.session['user_role'] = "job_seeker"
            jobs = Job.objects.order_by('-job_createdtime')  # Retrieve all job objects from the database
            return render(request, 'home.html', {'jobs': jobs,'loginusername':username,'user_role':"job_seeker"}) # Redirect to home page after successful login
        else:
            user = Recruiter.objects.filter(username=username, password=password).first()
            if user is not None:
                request.session['loginusername'] = username
                request.session['user_role'] = "recruiter"
                jobs = Job.objects.order_by('-job_createdtime')  # Retrieve all job objects from the database
                return render(request, 'home.html', {'jobs': jobs,'loginusername':username,'user_role':'recruiter'})
            else:
                return render(request, 'login.html', {'message': 'error'})
    else:
        return render(request, 'login.html')
    
def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        resume = request.POST.get('resume')
        cover_letter = request.POST.get('cover_letter')
        new_job = UserProfile.objects.create(
                username=username,
                password=password,
                full_name=full_name,
                email=email,
                phone=phone,
                resume=resume,
                cover_letter=cover_letter,
            )
        messages.success(request, 'user created successfully!')
        return redirect('login')
    return render(request, 'signup_jobseeker.html')

def signup_recruiter(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        company_name = request.POST.get('company_name')
        phone = request.POST.get('phone')
        new_job = Recruiter.objects.create(
                username=username,
                password=password,
                email=email,
                company_name=company_name,
                phone=phone
            )
        messages.success(request, 'user created successfully!')
        return redirect('login')
    return render(request, 'signup_recruiter.html')

def logout_view(request):
    # logout(request)
    return redirect('login')  # Redirect to the login page after logout

def signup_select(request):
    return render(request, 'signup_select.html')

def all_applicants(request):
    user_profile = request.session.get('loginusername') 
    user_role = request.session.get('user_role')
    application_Data = Application.objects.all()
    return render(request, 'all_applicants.html',{'loginusername':user_profile,"application_Data":application_Data,'user_role':user_role})

def track_applications(request):
    user_profile = request.session.get('loginusername') 
    user_role = request.session.get('user_role')
    application_Data = Application.objects.filter(username=user_profile).values()
    return render(request, 'track_applications.html',{'loginusername':user_profile,"application_Data":application_Data,'user_role':user_role})

@login_required
def profile(request):
    # Retrieve the profile data of the currently logged-in user
    user_profile = request.session.get('loginusername') 
    user_role = request.session.get('user_role')
    # user_profile = request.user  # Assuming profile is linked to the CustomUser model through a OneToOneField
    profileExist = UserProfile.objects.filter(username=user_profile).first()
    if profileExist is not None:
        profile = UserProfile.objects.filter(username=user_profile).values()
    else:
        profileExist = Recruiter.objects.filter(username=user_profile).first()
        if profileExist is not None:
            profile = Recruiter.objects.filter(username=user_profile).values()

    return render(request, 'profile.html',{'profile':profile,'loginusername':user_profile,'user_role':user_role})
    

@login_required
def home(request):
    user_profile = request.session.get('loginusername')
    user_role = request.session.get('user_role')
    jobs = Job.objects.order_by('-job_createdtime')  # Retrieve all job objects from the database
    return render(request, 'home.html', {'jobs': jobs,'loginusername':user_profile,'user_role':user_role})

# @login_required        
def search_results(request):
    user_profile = request.session.get('loginusername') 
    query = request.GET.get('query')
    user_role = request.session.get('user_role')
    # Perform the search query using the query parameter
    jobs = Job.objects.filter(job_description__icontains=query)
    return render(request, 'home.html', {'jobs': jobs,'loginusername':user_profile,'user_role':user_role})

# @login_required 
def addJob(request):
    user_profile = request.session.get('loginusername') 
    user_role = request.session.get('user_role')
    if request.method == 'POST':
        job_title = request.POST.get('jobTitle')
        company_name = request.POST.get('companyName')
        job_description = request.POST.get('jobDescription')
        job_location = request.POST.get('jobLocation')
        job_type = request.POST.get('jobType')

        # Create a new job instance and save it to the database
        new_job = Job.objects.create(
            job_title=job_title,
            company_name=company_name,
            job_description=job_description,
            job_location=job_location,
            job_type=job_type
        )
        messages.success(request, 'Job added successfully!')
        # Optionally, you can redirect to a success page
        return redirect('home')

    return render(request,"addJob.html",{'loginusername':user_profile,'user_role':user_role})


def apply_for_job(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        job_title = request.POST.get('job')
        company_name = request.POST.get('company_name')
        
        application = Application(username=username, job=job_title,company_name=company_name, status='Pending')
        application.save()
        
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False})
    
def update_application_status(request):
    if request.method == 'POST':
        try:
            application_id = request.POST.get('applicationId')
            status = request.POST.get('status')
            application = Application.objects.get(pk=application_id)
            application.status = status
            application.save()
            return JsonResponse({'message': 'Application status updated successfully'}, status=200)
        except Application.DoesNotExist:
            return JsonResponse({'error': 'Application not found'}, status=404)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)