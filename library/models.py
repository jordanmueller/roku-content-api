import datetime
from django.db import models
from django.utils import timezone

# set up some content type lookups
CONTENT_TYPE_CHOICES = (
        ('series', 'series'),
        ('episode', 'episode'),
)

class Category(models.Model):
    category_type = models.CharField(max_length=100, unique=True)

    def __unicode__(self):
        return self.category_type

    class Meta:
        verbose_name_plural = "categories"

class Course(models.Model):
    title = models.CharField(max_length=200)
    number = models.CharField(max_length=20)
    description = models.TextField()
    lecturer_firstname  = models.CharField('Lecturer Firstname', max_length=100)
    lecturer_lastname  = models.CharField('Lecturer Lastname', max_length=100)
    content_type = models.CharField('content type', 
                                    choices=CONTENT_TYPE_CHOICES,
                                    max_length=20)
    start_date = models.DateTimeField('date course started')
    end_date = models.DateTimeField('date course ended')
    release_date = models.DateTimeField('release date')
    course_poster_url = models.CharField('poster URL', max_length=500)
    categories = models.ManyToManyField(Category)

    def __unicode__(self):
        return self.number + ": " + self.title

class Lecture(models.Model):
    course = models.ForeignKey(Course)
    title = models.CharField(max_length=200)
    description = models.TextField()
    lecture_date = models.DateTimeField('lecture date')
    release_date = models.DateTimeField('release date')
    length = models.IntegerField()
    stream_url = models.CharField(max_length=500)
    stream_format = models.CharField(max_length=20)
    stream_qualities = models.CharField(max_length=20)
    stream_bitrate = models.IntegerField()

    def __unicode__(self):
        return self.title
