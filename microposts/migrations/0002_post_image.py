# Generated by Django 3.2.4 on 2024-11-18 04:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('microposts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, upload_to='images/'),
        ),
    ]
