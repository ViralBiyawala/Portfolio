# Generated by Django 5.0.3 on 2024-03-22 09:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('viralapp', '0015_remove_projects_live_link_projects_project'),
    ]

    operations = [
        migrations.RenameField(
            model_name='projects',
            old_name='project',
            new_name='live_link',
        ),
    ]
