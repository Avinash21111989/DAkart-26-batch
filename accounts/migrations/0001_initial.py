# Generated by Django 5.1.3 on 2024-12-07 02:12

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address_line_1', models.TextField(blank=True, max_length=500)),
                ('address_line_2', models.TextField(blank=True, max_length=500)),
                ('profile_picture', models.ImageField(blank=True, upload_to='userprofile')),
                ('city', models.CharField(max_length=20)),
                ('state', models.CharField(max_length=20)),
                ('country', models.CharField(max_length=20)),
                ('zipcode', models.IntegerField(max_length=10)),
                ('phoneno', models.IntegerField(max_length=10)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
