# Generated by Django 5.0.2 on 2024-03-16 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('viralapp', '0003_blogentry'),
    ]

    operations = [
        migrations.AlterField(
            model_name='education',
            name='graduation_year',
            field=models.CharField(max_length=200),
        ),
    ]