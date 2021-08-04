# Generated by Django 3.2.6 on 2021-08-04 17:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import tinymce.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=100, null=True)),
                ('description', models.TextField()),
                ('date_created', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.CharField(max_length=250)),
                ('photo_path', models.ImageField(upload_to='Profiles/')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='userprofile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TechNews',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', tinymce.models.HTMLField()),
                ('image_path', models.ImageField(upload_to='Stories/')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('link', models.CharField(blank=True, max_length=250, null=True)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.userprofile')),
            ],
        ),
        migrations.CreateModel(
            name='Stories',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', tinymce.models.HTMLField()),
                ('image_path', models.ImageField(upload_to='Stories/')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('link', models.CharField(blank=True, max_length=250, null=True)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.userprofile')),
            ],
        ),
        migrations.CreateModel(
            name='Idea',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', tinymce.models.HTMLField()),
                ('image1_path', models.ImageField(upload_to='Ideas/')),
                ('image2_path', models.ImageField(blank=True, null=True, upload_to='Ideas/')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('validity', models.DateField()),
                ('is_open', models.BooleanField(default=True)),
                ('collaborators', models.ManyToManyField(to='app.UserProfile')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='owner', to='app.userprofile')),
            ],
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('is_private', models.BooleanField(default=False)),
                ('admin', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='admin', to='app.userprofile')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('discussion', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.message')),
                ('members', models.ManyToManyField(to='app.UserProfile')),
            ],
            options={
                'ordering': ['date_created'],
            },
        ),
        migrations.CreateModel(
            name='GeneralAdmin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_general_admin', models.BooleanField(default=True)),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.userprofile')),
            ],
        ),
        migrations.CreateModel(
            name='Fundraiser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('image_path', models.ImageField(upload_to='Fundraisers/')),
                ('event_date', models.DateField()),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.userprofile')),
            ],
        ),
        migrations.CreateModel(
            name='Donor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('occupation', models.CharField(max_length=50)),
                ('is_alumni', models.BooleanField()),
                ('pledge', models.TextField()),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('fundaraiser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.fundraiser')),
            ],
        ),
    ]
