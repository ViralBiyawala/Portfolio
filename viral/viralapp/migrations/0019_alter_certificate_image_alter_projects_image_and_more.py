# Generated by Django 5.0.3 on 2024-04-02 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('viralapp', '0018_education_display_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='certificate',
            name='image',
            field=models.ImageField(upload_to='../media/images/certificate/'),
        ),
        migrations.AlterField(
            model_name='projects',
            name='image',
            field=models.ImageField(upload_to='../media/images/project_images/'),
        ),
        migrations.AlterField(
            model_name='resume',
            name='resume_file',
            field=models.FileField(upload_to='../media/files/resume/'),
        ),
    ]
