# Generated by Django 5.0.3 on 2024-03-21 17:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('viralapp', '0008_alter_certificate_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='certificate',
            name='image',
            field=models.ImageField(upload_to='static/images/certificate/'),
        ),
    ]