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

class Certificate(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='static/images/certificate/')
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

class Projects(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='static/images/project_images/')
    description = models.TextField()
    project_type = models.TextField()
    code_link = models.URLField(blank=True)
    live_link = models.URLField(blank=True)
    display_order = models.PositiveIntegerField()
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if self.pk:  
            old_certificate = Certificate.objects.get(pk=self.pk)
            if self.image != old_certificate.image:
                if old_certificate.image:
                    if os.path.isfile(old_certificate.image.path):
                        os.remove(old_certificate.image.path)
        super().save(*args, **kwargs)

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
