# Generated by Django 5.0.2 on 2024-03-16 15:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('viralapp', '0002_remove_intro_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('content', models.TextField()),
            ],
        ),
    ]
