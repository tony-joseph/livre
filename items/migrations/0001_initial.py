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
            name='BookCopy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('book_status', models.IntegerField(choices=[(1, 'Available'), (2, 'In Circulation'), (3, 'Temporarily Unavailable'), (4, 'Unavailable'), (5, 'Protected'), (6, 'Damaged')])),
                ('remarks', models.TextField(blank=True, default='')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='BookDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=1024)),
                ('author', models.CharField(default='Unknown', max_length=1024)),
                ('description', models.TextField(blank=True, default='')),
                ('publisher', models.CharField(blank=True, default='', max_length=512)),
                ('published_on', models.DateField(blank=True, null=True)),
                ('pages', models.PositiveIntegerField(blank=True, default=0, null=True)),
                ('ddc', models.CharField(blank=True, default='', max_length=1024)),
                ('llcc', models.CharField(blank=True, default='', max_length=1024)),
                ('isbn', models.CharField(blank=True, default='', max_length=1024)),
                ('tags', models.CharField(blank=True, max_length=1024, null=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=512)),
                ('slug', models.SlugField(max_length=128, unique=True)),
                ('description', models.TextField(blank=True, default='')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='category_updated_by', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=512)),
                ('short_code', models.CharField(db_index=True, max_length=8, unique=True)),
                ('description', models.TextField(blank=True, default='')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='language_updated_by', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Periodical',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=1024)),
                ('description', models.TextField(blank=True, default='')),
                ('publisher', models.CharField(blank=True, default='', max_length=512)),
                ('tags', models.CharField(blank=True, max_length=1024, null=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='items.Category')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('language', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='items.Language')),
                ('updated_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='periodical_updated_by', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PeriodicalIssue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('issue_status', models.IntegerField(choices=[(1, 'Available'), (2, 'In Circulation'), (3, 'Temporarily Unavailable'), (4, 'Unavailable'), (5, 'Protected'), (6, 'Damaged')])),
                ('published_on', models.DateField(blank=True, null=True)),
                ('volume', models.PositiveIntegerField(blank=True, null=True)),
                ('issue', models.PositiveIntegerField(blank=True, null=True)),
                ('remarks', models.TextField(blank=True, default='')),
                ('tags', models.CharField(blank=True, max_length=1024, null=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('periodical', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='items.Periodical')),
                ('updated_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='periodical_issue_updated_by', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='bookdetail',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='items.Category'),
        ),
        migrations.AddField(
            model_name='bookdetail',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='bookdetail',
            name='language',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='items.Language'),
        ),
        migrations.AddField(
            model_name='bookdetail',
            name='updated_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='book_detail_updated_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='bookcopy',
            name='book_detail',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='items.BookDetail'),
        ),
        migrations.AddField(
            model_name='bookcopy',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='bookcopy',
            name='updated_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='book_copy_updated_by', to=settings.AUTH_USER_MODEL),
        ),
    ]