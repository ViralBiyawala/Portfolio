# Generated by Django 5.0.3 on 2024-04-01 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('viralapp', '0016_rename_project_projects_live_link'),
    ]

    operations = [
        migrations.CreateModel(
            name='Resume',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('resume_file', models.FileField(upload_to='static/files/resume/')),
            ],
        ),
    ]