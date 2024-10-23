# viralapp/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import logout
from .models import Intro, BlogEntry, Education, Skills, Certificate, Projects, Resume, WorkExperience
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.http import JsonResponse
from .forms import CertificateForm, ProjectsForm, ResumeForm
import json
import os
from django.apps import apps
import requests

import re
from werkzeug.utils import secure_filename

def remove_repeated_end_phrases(response, num_words=5):
    # Remove any text after the first newline character
    response = response.split('\n')[0]

    # Split the response into sentences
    sentences = response.split(". ")

    # To keep the cleaned sentences
    cleaned_sentences = []

    # Process each sentence
    for current_sentence in sentences:
        current_sentence = current_sentence.strip()
        if cleaned_sentences:
            # Last sentence added to cleaned_sentences
            last_cleaned_sentence = cleaned_sentences[-1].strip()
            # Get the last num_words from the last cleaned sentence
            last_words = ' '.join(last_cleaned_sentence.split()[-num_words:])

            # Check if the current sentence ends with the last words of the previous sentence
            if last_words and current_sentence.endswith(last_words):
                # If it does, skip the current sentence
                continue

        cleaned_sentences.append(current_sentence)

    # Join the cleaned sentences back together
    filtered_response = ". ".join(cleaned_sentences).strip()
    return filtered_response

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

    intro_split = intro.content.split('\n')

    # print(superuser)
    allowed_extensions = ['jpg', 'jpeg', 'png']

    src = "/media/images/profile.jpg"
    # Check if an image file exists for the user
    for extension in allowed_extensions:
        image_path = f"/media/images/profile.{extension}"
        if os.path.isfile(image_path) == True:
            src = f"/media/images/profile.{extension}"
            break

    # editable = False
    # editable = True

    blog_entries = BlogEntry.objects.all()
    mark = 'promark'

    context = {
        'theme_preference': theme_preference,
        'user': superuser,
        'is_superuser': True,
        'link':src,
        'intro': intro,
        'intro_split': intro_split,
        # 'mark': mark,
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
                image_path = f"/media/images/profile.{extension}"
                if os.path.isfile(image_path):
                    os.remove(image_path)

            # Generate a secure filename based on User_id and the file extension
            filename = f"profile{os.path.splitext(image.name)[1]}"
            filename = secure_filename(filename)
            image_path = os.path.join("/home/ViralBiyawala/Portfolio/viral/media/images", filename)

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

    src = "/media/images/profile.jpg"
    # Check if an image file exists for the user
    for extension in allowed_extensions:
        image_path = f"/media/images/profile.{extension}"
        if os.path.isfile(image_path) == True:
            src = f"/media/images/profile.{extension}"
            break

    # editable = False
    # editable = True

    blog_entries = BlogEntry.objects.all()
    
    mark = 'promark'

    context = {
        'theme_preference': theme_preference,
        'user': superuser,
        'is_superuser': True,
        'link':src,
        'intro': intro,
        'intro_split': intro_split,
        'mark': mark,
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

    # Get education entries for the superuser
    education_entries = Education.objects.filter(user=superuser).order_by('-display_order')
    
    # Get skills entries
    skills_entries = Skills.objects.filter(user=superuser)
    
    # Get work experience entries
    work_experience_entries = WorkExperience.objects.filter(user=superuser).order_by('-display_order')

    allowed_extensions = ['jpg', 'jpeg', 'png']
    src = "/media/images/profile.jpg"
    # Check if an image file exists for the user
    for extension in allowed_extensions:
        image_path = f"/media/images/profile.{extension}"
        if os.path.isfile(image_path):
            src = f"/media/images/profile.{extension}"
            break

    mark = 'promark'

    context = {
        'theme_preference': theme_preference,
        'user': superuser,
        'is_superuser': True,
        'link': src,
        'mark': mark,
        'education_entries': education_entries,
        'skills_entries': skills_entries,
        'work_experience_entries': work_experience_entries,
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

    src = "/media/images/profile.jpg"
    # Check if an image file exists for the user
    for extension in allowed_extensions:
        image_path = f"/media/images/profile.{extension}"
        if os.path.isfile(image_path) == True:
            src = f"/media/images/profile.{extension}"
            break

    # editable = False
    # editable = True

    certificates = Certificate.objects.all().order_by('display_order')
    mark = 'promark'

    context = {
        'theme_preference': theme_preference,
        'user': superuser,
        'is_superuser': True,
        'link':src,
        'certificates': certificates,
        'mark': mark,
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

    src = "/media/images/profile.jpg"
    # Check if an image file exists for the user
    for extension in allowed_extensions:
        image_path = f"/media/images/profile.{extension}"
        if os.path.isfile(image_path) == True:
            src = f"/media/images/profile.{extension}"
            break

    # editable = False
    # editable = True

    all_projects = Projects.objects.all().order_by('display_order')
    mark = 'promark'

    context = {
        'theme_preference': theme_preference,
        'user': superuser,
        'is_superuser': True,
        'link':src,
        'mark': mark,
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
        display_order = request.POST.get('display_order')

        # Associate the education entry with the current user
        Education.objects.create(user=User.objects.filter(is_superuser=True).first(), degree=degree, school=school, graduation_year=graduation_year, display_order=display_order)
        return redirect('education')

@csrf_exempt
def delete_education_entry(request):
    if request.method == 'POST':
        degree = request.POST.get('degree')
        school = request.POST.get('school')
        graduation_year = request.POST.get('graduation_year')
        Education.objects.filter(degree=degree, school=school, graduation_year=graduation_year).delete()
        return redirect('education')

@csrf_exempt
def add_work_experience(request):
    if request.method == 'POST':
        job_title = request.POST.get('job_title')
        company = request.POST.get('company')
        years = request.POST.get('years')
        display_order = request.POST.get('display_order')

        # Associate the work experience entry with the current user
        WorkExperience.objects.create(user=User.objects.filter(is_superuser=True).first(), job_title=job_title, company=company, years=years, display_order=display_order)
        return redirect('education')

@csrf_exempt
def delete_work_experience(request):
    if request.method == 'POST':
        job_title = request.POST.get('job_title')
        company = request.POST.get('company')
        years = request.POST.get('years')
        WorkExperience.objects.filter(job_title=job_title, company=company, years=years).delete()
        return redirect('education')

def custom_logout(request):
    logout(request)
    return redirect('index')

@csrf_exempt
def upload_resume(request):
    if request.method == 'POST':
        form = ResumeForm(request.POST, request.FILES)
        if form.is_valid():
            # Check if a resume entry already exists
            if Resume.objects.exists():
                resume = Resume.objects.first()
                resume.resume_file = form.cleaned_data['resume_file']
                resume.save()
            else:
                form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)
    else:
        form = ResumeForm()
    return render(request, 'upload_resume.html', {'form': form})

@csrf_exempt
def download_resume(request):
    resume = Resume.objects.first()  # Assuming there's only one resume file
    if resume:
        return redirect(resume.resume_file.url)
    else:
        return JsonResponse({'error': 'Resume not found'}, status=404)

def custom_404(request, exception):
    return render(request, '404.html', status=404)

@csrf_exempt
def ask(request):
    if request.method == "POST":
        # print("hit")
        try:
            data = json.loads(request.body)  # Load the JSON data from the request body
            user_query = data.get('query')  # Get the 'query' field
            # print(user_query)
        except json.JSONDecodeError:
            # print("error")
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        if user_query is None:
            return JsonResponse({'error': 'No query provided'}, status=400)

        # Make a POST request to the external Flask API
        try:
            # print("requesting")
            api_url = "https://viralbot.pythonanywhere.com/chatbot"  # Local Flask API URL
            payload = {"user_query": user_query}
            headers = {'Content-Type': 'application/json'}
            
            # Send POST request to Flask API
            external_response = requests.post(api_url, json=payload, headers=headers)
            print(external_response)

            if external_response.status_code == 200:
                # Extract response text
                external_data = external_response.json()
                chatbot_response = external_data.get('response', '')

                return JsonResponse({'response': chatbot_response})
            else:
                return JsonResponse({'error': 'Failed to fetch data from the external API'}, status=external_response.status_code)

        except requests.RequestException as e:
            return JsonResponse({'error': f'Error occurred while contacting external API: {str(e)}'}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)