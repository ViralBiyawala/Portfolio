# Generated by Django 5.0.3 on 2024-03-21 17:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('viralapp', '0007_alter_certificate_display_order_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='certificate',
            name='image',
            field=models.ImageField(upload_to='certificate/'),
        ),
    ]