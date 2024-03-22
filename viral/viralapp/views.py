# viralapp/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import logout
from .models import Intro, BlogEntry, Education, Skills, Certificate, Projects
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.http import JsonResponse
from .forms import CertificateForm, ProjectsForm
import json
import os

def dashboard_view(request):
# Get the superuser directly
    superuser = User.objects.filter(is_superuser=True).first()

    # Check if theme preference is toggled
    if 'theme_preference' in request.GET:
        theme_preference = request.GET['theme_preference']
        # Set the theme preference in the session
        request.session['theme_preference'] = theme_preference

    # Get the theme preference from the session or default to 'light'
    theme_preference = request.session.get('theme_preference', 'light')
    
    intro, created = Intro.objects.get_or_create(pk=1)
    
    if request.method == 'POST':
        content = request.POST.get('content', '')
        intro.content = content
        intro.save()
        return redirect('index')
    
    # print(superuser)
    allowed_extensions = ['jpg', 'jpeg', 'png']

    src = "../static/images/profile.jpg"
    # Check if an image file exists for the user
    for extension in allowed_extensions:
        image_path = f"viralapp/static/images/profile.{extension}"
        if os.path.isfile(image_path) == True:
            src = f"images/profile.{extension}"
            break
        
    # editable = False
    # editable = True
    
    blog_entries = BlogEntry.objects.all()
    
    context = {
        'theme_preference': theme_preference,
        'user': superuser,
        'is_superuser': True,
        'link':src,
        'intro': intro,
        # 'editable': editable,
        'blog_entries': blog_entries,
    }

    return render(request, 'dashboard.html', context)

@csrf_exempt
def update_img(request):
    if request.method == 'POST':
        image = request.FILES.get('image')
        if image:
            # Delete previous images with the same name but different extensions
            allowed_extensions = ['png', 'jpg', 'jpeg']
            for extension in allowed_extensions:
                image_path = f"viralapp/static/images/profile.{extension}"
                if os.path.isfile(image_path):
                    os.remove(image_path)

            # Generate a secure filename based on User_id and the file extension
            filename = f"profile{os.path.splitext(image.name)[1]}"
            image_path = os.path.join("viralapp/static/images", filename)

            # Ensure the directory exists
            os.makedirs(os.path.dirname(image_path), exist_ok=True)

            # Save the uploaded image with the User_id as the filename
            with open(image_path, 'wb') as destination:
                for chunk in image.chunks():
                    destination.write(chunk)

            messages.success(request, 'Image uploaded successfully.')
            return redirect('index')

    # Handle other cases or render a template
    return redirect('index')


def index(request):
# Get the superuser directly
    superuser = User.objects.filter(is_superuser=True).first()

    # Check if theme preference is toggled
    if 'theme_preference' in request.GET:
        theme_preference = request.GET['theme_preference']
        # Set the theme preference in the session
        request.session['theme_preference'] = theme_preference

    # Get the theme preference from the session or default to 'light'
    theme_preference = request.session.get('theme_preference', 'light')
    
    intro, created = Intro.objects.get_or_create(pk=1)
    
    if request.method == 'POST':
        content = request.POST.get('content', '')
        intro.content = content
        intro.save()
        return redirect('index')
    
    intro_split = intro.content.split('\n')
    
    # print(superuser)
    allowed_extensions = ['jpg', 'jpeg', 'png']

    src = "../static/images/profile.jpg"
    # Check if an image file exists for the user
    for extension in allowed_extensions:
        image_path = f"viralapp/static/images/profile.{extension}"
        if os.path.isfile(image_path) == True:
            src = f"images/profile.{extension}"
            break
        
    # editable = False
    # editable = True
    
    blog_entries = BlogEntry.objects.all()
    
    context = {
        'theme_preference': theme_preference,
        'user': superuser,
        'is_superuser': True,
        'link':src,
        'intro': intro,
        'intro_split': intro_split,
        # 'editable': editable,
        'blog_entries': blog_entries,
    }

    return render(request, 'dashboard.html', context)

@csrf_exempt
def update_blog_entry(request):
    # if request.method == 'POST':
    data = json.loads(request.body)
    title = data.get('title')
    content = data.get('content')
    BlogEntry.objects.create(title=title, content=content)
    return redirect('index')

@csrf_exempt
def delete_blog_entry(request):
    data = json.loads(request.body)
    title = data.get('title')
    content = data.get('content')
    if title and content:
        entry = BlogEntry.objects.filter(title=title, content=content).first()
        entry.delete()
    return redirect('index')


def education(request):
# Get the superuser directly
    superuser = User.objects.filter(is_superuser=True).first()

    # Check if theme preference is toggled
    if 'theme_preference' in request.GET:
        theme_preference = request.GET['theme_preference']
        # Set the theme preference in the session
        request.session['theme_preference'] = theme_preference

    # Get the theme preference from the session or default to 'light'
    theme_preference = request.session.get('theme_preference', 'light')
    
    # print(superuser)
    allowed_extensions = ['jpg', 'jpeg', 'png']
    
    education_entries = Education.objects.filter(user=User.objects.filter(is_superuser=True).first())
    skills_entries = Skills.objects.filter()

    src = "../static/images/profile.jpg"
    # Check if an image file exists for the user
    for extension in allowed_extensions:
        image_path = f"viralapp/static/images/profile.{extension}"
        if os.path.isfile(image_path) == True:
            src = f"images/profile.{extension}"
            break
        
    # editable = False
    # editable = True
    
    context = {
        'theme_preference': theme_preference,
        'user': superuser,
        'is_superuser': True,
        'link':src,
        'education_entries': education_entries,
        # 'editable': editable,
        'skills_entries': skills_entries,
    }

    return render(request, 'education.html', context)

@csrf_exempt
def add_skill(request):
    if request.method == 'POST':
        # Add a new skill entry
        skill_name = request.POST.get('skill', '')
        if skill_name:
            # Check if the skill already exists for the user
            if not Skills.objects.filter(user=User.objects.filter(is_superuser=True).first(), skills_list__iexact=skill_name).exists():
                Skills.objects.create(user=User.objects.filter(is_superuser=True).first(),skills_list=skill_name)
    return redirect('education')  

@csrf_exempt
def del_skill(request):
    if request.method == 'POST':
        skill_name = request.POST.get('skill', '')
        if skill_name and Skills.objects.filter(user=User.objects.filter(is_superuser=True).first(),skills_list__iexact=skill_name):
            # Delete the skill entry if it exists for the user
            Skills.objects.filter(user=User.objects.filter(is_superuser=True).first(),skills_list__iexact=skill_name).delete()
    return redirect('education')  

def certification(request):
# Get the superuser directly
    superuser = User.objects.filter(is_superuser=True).first()

    # Check if theme preference is toggled
    if 'theme_preference' in request.GET:
        theme_preference = request.GET['theme_preference']
        # Set the theme preference in the session
        request.session['theme_preference'] = theme_preference

    # Get the theme preference from the session or default to 'light'
    theme_preference = request.session.get('theme_preference', 'light')
    
    # print(superuser)
    allowed_extensions = ['jpg', 'jpeg', 'png']

    src = "../static/images/profile.jpg"
    # Check if an image file exists for the user
    for extension in allowed_extensions:
        image_path = f"viralapp/static/images/profile.{extension}"
        if os.path.isfile(image_path) == True:
            src = f"images/profile.{extension}"
            break
    
    # editable = False
    # editable = True
    
    certificates = Certificate.objects.all().order_by('display_order')
    
    context = {
        'theme_preference': theme_preference,
        'user': superuser,
        'is_superuser': True,
        'link':src,
        'certificates': certificates,
        # 'editable': editable,
    }

    return render(request, 'certification.html', context)


def add_certificate(request):
    if request.method == 'POST':
        form = CertificateForm(request.POST, request.FILES)
        if form.is_valid():
            certificate = form.save(commit=False)
            new_display_order = certificate.display_order
            
            # Adjust display order of existing certificates
            certificates_to_adjust = Certificate.objects.filter(display_order__gte=new_display_order)
            for cert in certificates_to_adjust:
                cert.display_order += 1
                cert.save()
            
            certificate.save()
            return JsonResponse({'success': True})
        else:
            return redirect('certification')
    return JsonResponse({'success': False, 'errors': 'Invalid request method'})

def delete_certificate(request, pk):
    certificate = get_object_or_404(Certificate, pk=pk)
    certificate.delete()
    return redirect('certification')

@csrf_exempt
def update_certificate(request, pk):
    certificate = get_object_or_404(Certificate, pk=pk)
    if request.method == 'POST':
        form = CertificateForm(request.POST, request.FILES, instance=certificate)
        if form.is_valid():
            certificate = form.save(commit=False)
            new_display_order = certificate.display_order
            
            # Adjust display order of existing certificates
            certificates_to_adjust = Certificate.objects.filter(display_order__gte=new_display_order)
            for cert in certificates_to_adjust:
                cert.display_order += 1
                cert.save()
            
            certificate.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    return JsonResponse({'success': False, 'errors': 'Invalid request method'})

def project(request):
# Get the superuser directly
    superuser = User.objects.filter(is_superuser=True).first()

    # Check if theme preference is toggled
    if 'theme_preference' in request.GET:
        theme_preference = request.GET['theme_preference']
        # Set the theme preference in the session
        request.session['theme_preference'] = theme_preference

    # Get the theme preference from the session or default to 'light'
    theme_preference = request.session.get('theme_preference', 'light')
    
    # print(superuser)
    allowed_extensions = ['jpg', 'jpeg', 'png']

    src = "../static/images/profile.jpg"
    # Check if an image file exists for the user
    for extension in allowed_extensions:
        image_path = f"viralapp/static/images/profile.{extension}"
        if os.path.isfile(image_path) == True:
            src = f"images/profile.{extension}"
            break
        
    # editable = False
    # editable = True
    
    all_projects = Projects.objects.all().order_by('display_order')
    
    context = {
        'theme_preference': theme_preference,
        'user': superuser,
        'is_superuser': True,
        'link':src,
        # 'editable': editable,
        'all_projects': all_projects,
    }

    return render(request, 'project.html', context)

def add_project(request):
    if request.method == 'POST':
        form = ProjectsForm(request.POST, request.FILES)
        if form.is_valid():
            Projectfr = form.save(commit=False)
            new_display_order = Projectfr.display_order
            
            # Adjust display order of existing Projectss
            Projectss_to_adjust = Projects.objects.filter(display_order__gte=new_display_order)
            for pro in Projectss_to_adjust:
                pro.display_order += 1
                pro.save()
            
            Projectfr.save()
            return JsonResponse({'success': True})
        else:
            return redirect('project')
    return JsonResponse({'success': False, 'errors': 'Invalid request method'})

def delete_project(request, pk):
    project = get_object_or_404(Projects, pk=pk)
    project.delete()
    return redirect('project')

@csrf_exempt
def update_project(request, pk):
    project = get_object_or_404(Projects, pk=pk)
    if request.method == 'POST':
        form = ProjectsForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            project = form.save(commit=False)
            new_display_order = project.display_order
            
            # Adjust display order of existing certificates
            project_to_adjust = Projects.objects.filter(display_order__gte=new_display_order)
            for pro in project_to_adjust:
                pro.display_order += 1
                pro.save()
            
            project.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    return JsonResponse({'success': False, 'errors': 'Invalid request method'})


@csrf_exempt
def add_education_entry(request):
    if request.method == 'POST':
        degree = request.POST.get('degree')
        school = request.POST.get('school')
        graduation_year = request.POST.get('graduation_year')
        
        # Associate the education entry with the current user
        Education.objects.create(user=User.objects.filter(is_superuser=True).first(), degree=degree, school=school, graduation_year=graduation_year)
        # return JsonResponse({'message': 'Education entry added successfully'})
        return redirect('education')

@csrf_exempt
def delete_education_entry(request):
    if request.method == 'POST':
        degree = request.POST.get('degree')
        school = request.POST.get('school')
        graduation_year = request.POST.get('graduation_year')
        Education.objects.filter(degree=degree, school=school, graduation_year=graduation_year).delete()
        # return JsonResponse({'message': 'Education entry deleted successfully'})
        return redirect('education')

def custom_logout(request):
    logout(request)
    return redirect('index')