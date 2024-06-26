# Generated by Django 5.0.3 on 2024-03-22 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('viralapp', '0012_certificate_link'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='projects',
            name='user',
        ),
        migrations.AddField(
            model_name='projects',
            name='project_type',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='projects',
            name='image',
            field=models.ImageField(upload_to='static/images/project_images/'),
        ),
    ]
