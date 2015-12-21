# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-21 12:22
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Not specified', 'Not Specified')], default='Not specified', max_length=50)),
                ('birthday', models.DateField(blank=True, null=True)),
                ('phone', models.CharField(blank=True, max_length=24, null=True)),
                ('city', models.CharField(blank=True, max_length=150, null=True)),
                ('state', models.CharField(blank=True, max_length=150, null=True)),
                ('country', models.CharField(blank=True, max_length=150, null=True)),
                ('zip_code', models.CharField(blank=True, max_length=8, null=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]