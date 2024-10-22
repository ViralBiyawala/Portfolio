# viralapp/models.py

from django.db import models
from django.contrib.auth.models import User
import os

class Intro(models.Model):
    content = models.TextField()
    
class BlogEntry(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()

    def __str__(self):
        return self.title

class Education(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    degree = models.CharField(max_length=200)
    school = models.CharField(max_length=200)
    graduation_year = models.CharField(max_length=200)
    display_order = models.IntegerField(default=0, blank=True, null=True)

    def save(self, *args, **kwargs):
        # Check if there is any existing entry with the same display order
        existing_entries = Education.objects.filter(display_order=self.display_order)
        
        if existing_entries.exists():
            # Increment display_order for each entry after the new display order
            for entry in existing_entries:
                entry.display_order += 1
                entry.save()  # Save each entry with updated display order
        
        super().save(*args, **kwargs)

class Certificate(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='certificate/')
    issued_by = models.CharField(max_length=100)
    date_awarded = models.DateField()
    expiry_date = models.DateField(blank=True, null=True)
    skills_gained = models.TextField()
    link = models.TextField( blank=True, null=True)
    display_order = models.IntegerField(default=0, blank=True, null=True)

    def __str__(self):
        return self.title

    def get_skills(self):
        return [skill.strip() for skill in self.skills_gained.split(',') if skill]

    def set_skills(self, skills):
        self.skills = ','.join(skill.strip() for skill in skills)
        
    def delete(self, *args, **kwargs):
        if self.image:
            if os.path.isfile(self.image.path):
                os.remove(self.image.path)
        super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        if self.pk:  
            old_certificate = Certificate.objects.get(pk=self.pk)
            if self.image != old_certificate.image:
                if old_certificate.image:
                    if os.path.isfile(old_certificate.image.path):
                        os.remove(old_certificate.image.path)
        super().save(*args, **kwargs)

from django.db import models

class Projects(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='project_images/')
    description = models.TextField()
    project_type = models.TextField(blank=True)
    code_link = models.URLField(blank=True)
    code_type = models.TextField(blank=True)
    live_link = models.URLField(blank=True)
    display_order = models.PositiveIntegerField()
    
    def __str__(self):
        return self.title
    
    def delete(self, *args, **kwargs):
        if self.image:
            if os.path.isfile(self.image.path):
                os.remove(self.image.path)
        super().delete(*args, **kwargs)
    
    def save(self, *args, **kwargs):
        if self.pk:  
            old_project = Projects.objects.get(pk=self.pk)
            if self.image != old_project.image:
                if old_project.image:
                    if os.path.isfile(old_project.image.path):
                        os.remove(old_project.image.path)
        super().save(*args, **kwargs)

class Resume(models.Model):
    resume_file = models.FileField(upload_to='files/resume/')

    def save(self, *args, **kwargs):
        if self.id:
            try:
                old_instance = Resume.objects.get(pk=self.id)
                old_instance.resume_file.delete(save=False)
            except Resume.DoesNotExist:
                pass
        super(Resume, self).save(*args, **kwargs)


class Skills(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    skills_list = models.CharField(max_length=2048, blank=True)

    def get_skills(self):
        return [skill.strip() for skill in self.skills_list.split(',') if skill]

    def set_skills(self, skills):
        self.skills_list = ','.join(skill.strip() for skill in skills)


class Contact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()

class WorkExperience(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job_title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    years = models.CharField(max_length=50)
    display_order = models.IntegerField(default=0, blank=True, null=True)

    def __str__(self):
        return f"{self.job_title} at {self.company}"
    
    def save(self, *args, **kwargs):
        if self.pk:
            old_instance = WorkExperience.objects.get(pk=self.pk)
            if self.display_order != old_instance.display_order:
                existing_entries = WorkExperience.objects.filter(display_order=self.display_order)
                if existing_entries.exists():
                    for entry in existing_entries:
                        entry.display_order += 1
                        entry.save()
        super().save(*args, **kwargs)