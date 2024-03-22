# viralapp/urls.py

from django.urls import path
from . import views
# from .views import dashboard_view, update_img, index, education, certification, project, update_blog_entry, delete_blog_entry, add_education_entry, delete_education_entry, add_skill, del_skill, add_certificate

urlpatterns = [
    # Add other URLs as needed
    path('', views.dashboard_view, name='dashboard'),
    path('index/', views.index, name='index'),
    path('update_img/', views.update_img, name='update_img'),
    path('education/', views.education, name='education'),
    path('certification/', views.certification, name='certification'),
    path('project/', views.project, name='project'),
    path('update_blog_entry/', views.update_blog_entry, name='update_blog_entry'),
    path('delete_blog_entry/', views.delete_blog_entry, name='delete_blog_entry'),
    path('add_education_entry/', views.add_education_entry, name='add_education_entry'),
    path('delete_education_entry/', views.delete_education_entry, name='delete_education_entry'),
    path('add_skill/', views.add_skill, name='add_skill'),
    path('del_skill/', views.del_skill, name='del_skill'),
    path('add_certificate/', views.add_certificate, name='add_certificate'),
    path('certificates/<int:pk>/delete/', views.delete_certificate, name='delete_certificate'),
    path('update_certificate/<int:pk>/', views.update_certificate, name='update_certificate'),
    path('add_project/', views.add_project, name='add_project'),
    path('project/<int:pk>/delete/', views.delete_project, name='delete_project'),
    path('update_project/<int:pk>/', views.update_project, name='update_project'),
    
]
