# Models.py defines the data model for the HarvardTV system.
#
# The models are Category, Course, and Lecture.

import datetime
from django.db import models
from django.utils import timezone

# set up some content type lookups used in the
# Course model
CONTENT_TYPE_CHOICES = (
        ('series', 'series'),
        ('episode', 'episode'),
)


# The Category model is simply a list of categories in the system.
# Examples are: Computer Science, History, Mathematics, etc.
class Category(models.Model):
    category_type = models.CharField(max_length=100, unique=True)

    # to_string of the model.
    def __unicode__(self):
        return self.category_type

    # Define the pluralization of the class, otherwise category would
    # pluralize as categorys.
    class Meta:
        verbose_name_plural = "categories"

# The Course model defines each course that hase lectures
# in the HarvardTV system. 
class Course(models.Model):

    # Course and Category are in a many to many relationship
    categories = models.ManyToManyField(Category)

    # Course data elements
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

    # to_string
    def __unicode__(self):
        return self.number + ": " + self.title

# The lecture model defines each lecture available to stream
class Lecture(models.Model):

    # Lectures are in a many to one relationship with Course
    course = models.ForeignKey(Course)

    # Lecture data elements
    title = models.CharField(max_length=200)
    description = models.TextField()
    lecture_date = models.DateTimeField('lecture date')
    release_date = models.DateTimeField('release date')
    length = models.IntegerField()
    stream_url = models.CharField(max_length=500)
    stream_format = models.CharField(max_length=20)
    stream_qualities = models.CharField(max_length=20)
    stream_bitrate = models.IntegerField()

    # to_string
    def __unicode__(self):
        return self.title
