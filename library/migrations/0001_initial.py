# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('category_type', models.CharField(unique=True, max_length=100)),
            ],
            options={
                'verbose_name_plural': 'categories',
            },
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200)),
                ('number', models.CharField(max_length=20)),
                ('description', models.TextField()),
                ('lecturer_firstname', models.CharField(max_length=100, verbose_name=b'Lecturer Firstname')),
                ('lecturer_lastname', models.CharField(max_length=100, verbose_name=b'Lecturer Lastname')),
                ('content_type', models.CharField(max_length=20, verbose_name=b'content type', choices=[(b'series', b'series'), (b'episode', b'episode')])),
                ('start_date', models.DateTimeField(verbose_name=b'date course started')),
                ('end_date', models.DateTimeField(verbose_name=b'date course ended')),
                ('release_date', models.DateTimeField(verbose_name=b'release date')),
                ('course_poster_url', models.CharField(max_length=500, verbose_name=b'poster URL')),
                ('categories', models.ManyToManyField(to='library.Category')),
            ],
        ),
        migrations.CreateModel(
            name='Lecture',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('lecture_date', models.DateTimeField(verbose_name=b'lecture date')),
                ('release_date', models.DateTimeField(verbose_name=b'release date')),
                ('length', models.IntegerField()),
                ('stream_url', models.CharField(max_length=500)),
                ('stream_format', models.CharField(max_length=20)),
                ('stream_qualities', models.CharField(max_length=20)),
                ('stream_bitrate', models.IntegerField()),
                ('course', models.ForeignKey(to='library.Course')),
            ],
        ),
    ]
