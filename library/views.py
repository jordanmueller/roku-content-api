# The views.py module defines the main behavior of the HarvardTV webservice.
#
# Each method retrieves request sepcific data from the Django models, structures
# the data appropriately, and sends it back to the client as a JSON response.
#
# Each request is routed to a specific method here by pattern matching in the
# urls.py module.
#
# Parameters are passed as named parameters from the urls.py module.  The names 
# in the method signature, must match the names of the parameters in the 
# urls.py regular expressions.  For example, ?P<course_id> in the URL match 
# must correspond to a course_id parameter defined in the associated views.py 
# method signature.
#
# This module makes heavy use of the reverse() method from django.core.urlresolvers.
# It is a reverse lookup of the URL -> View mapping defined in urls.py.  Arguments to
# revers() are a view method name and optional arguments.  Reverse() looks through the
# urls.py definitions to build a URL path that will match the specific view method. 
# This is how the response gives the client URLs for other resources in the web service.
#

from django import http
from datetime import datetime
from django.utils import simplejson as json
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.db.models import Q
from library.models import Category, Course, Lecture

#   method: category_list 
#   params: none
# response: JSON Array of objects describing each category in the system
#
def category_list(request):
    category_list = []

    # iterate over the catagory objects and
    # build an array of hashes for the reponse
    for category in Category.objects.all():
        category_info = {}
        category_info['id'] = category.id
        category_info['name'] = category.category_type
        category_info['url']   = ('http://' + request.get_host() + 
                                    reverse('library.views.category_detail', 
                                            args=(category.id,))
                                )

        category_list.append(category_info)

    # Dump the array to JSON and send the response.
    return http.HttpResponse(json.dumps(category_list), 
                             mimetype='application/json')

#   method: category_detail
#   params: category_id
# response: JSON Array of objects describing each course in the category
#           identified by category_id.
#
def category_detail(request, category_id):

    # Find object or redirect to 404 page if it doesn't exist.
    category = get_object_or_404(Category, pk=category_id)

    course_list = []
    
    # Iterate over the courses building an array of hashes
    for course in category.course_set.all():
        course_info = {}
        course_info['id'] = str(course.id)
        course_info['title'] = course.title
        course_info['number'] = course.number
        course_info['description'] = course.description
        course_info['release_date'] = course.release_date.strftime("%m/%d/%y")
        course_info['url']   = ('http://' + request.get_host() + 
                                reverse('library.views.course_detail', 
                                args=(course.id,))
                               )
        course_info['SDPosterUrl'] = course.course_poster_url

        course_list.append(course_info)

    # convert array to JSON and send the response
    return http.HttpResponse(json.dumps(course_list), 
                             mimetype='application/json')

#   method: course_list
#   params: none
# response: A JSON array of objects.  Each object describes a specific
#           course in the system.
#
def course_list(request):
    course_list = []

    # Iterate over the courses building an array of hashes
    for course in Course.objects.all():
        course_info = {}
        course_info['id'] = course.id
        course_info['title'] = course.title
        course_info['url']   = ('http://' + request.get_host() + 
                                reverse('library.views.course_detail', 
                                args=(course.id,))
                               )

        course_list.append(course_info)

    # convert array to JSON and send the response
    return http.HttpResponse(json.dumps(course_list), 
                             mimetype='application/json')


#   method: course_detail
#   params: course_id
# response: A JSON object describing the details of a specific course.
#    notes: The JSON object includes an ARRAY of each lecture availible in the
#           specific course. It's the lectures element of the course object.
#
def course_detail(request, course_id):

    # Find object or redirect to 404 page if it doesn't exist.
    c = get_object_or_404(Course, pk=course_id)

    # Convert non-string values (int, dates, objects, etc) to strings
    # for JSON output
    course = {}
    for key, value in c.__dict__.iteritems():
        if isinstance( value, unicode ):
            course[key] = value
        elif isinstance( value, int):
            course[key] = str(value)
        elif isinstance( value, datetime ):
            course[key] = value.strftime("%m/%d/%y")

    course['lectures'] = []

    # Add the lecture info as hashes in the course['lectures'] array
    for l in c.lecture_set.all():
        lecture = {}
        lecture['title'] = l.title
        lecture['id']    = l.id
        lecture['description'] = l.description
        lecture['url']   = ('http://' + request.get_host() + 
                            reverse('library.views.lecture_detail', 
                                    args=(c.id,l.id,))
                           )
        lecture['SDPosterUrl'] = c.course_poster_url
        course['lectures'].append(lecture)

    # convert hash to JSON and send the response
    return http.HttpResponse(json.dumps(course), 
                             mimetype='application/json')
    
#   method: lecture_list
#   params: course_id
# response: A JSON array of lecture objects for a specific course.
#    notes: This data is the same as the "lectures" element in the
#           course_details method
#
def lecture_list(request, course_id):
    lecture_list = []

    # iterate over the lectures builing up an array of hashes
    for lecture in Lecture.objects.filter(course__id=course_id):
        lecture_info = {}

        lecture_info['id'] = lecture.id
        lecture_info['title'] = lecture.title
        lecture_info['description'] = lecture.description
        lecture_info['url']   = ('http://' + request.get_host() + 
                                    reverse('library.views.lecture_detail', 
                                            args=(course_id,lecture.id,))
                                )

        lecture_list.append(lecture_info)

    # send it back as JSON
    return http.HttpResponse(json.dumps(lecture_list), 
                             mimetype='application/json')



#   method: lecture_detail
#   params: course_id, lecture_id
# response: A JSON Object decribing the specific lecture details
#
def lecture_detail(request, course_id, lecture_id):
    l = get_object_or_404(Lecture, pk=lecture_id)

    lecture = {}
    # Convert non-string values (int, dates, objects, etc) to strings
    # for JSON output
    for key, value in l.__dict__.iteritems():
        if isinstance( value, unicode ):
            lecture[key] = value
        elif isinstance( value, int):
            lecture[key] = str(value)
        elif isinstance( value, datetime ):
            lecture[key] = value.strftime("%m/%d/%y")

    lecture['course_title'] = l.course.title
    lecture['course_number'] = l.course.number

    # Add the categories for this lecture's course
    lecture['categories'] = []
    for category in l.course.categories.all():
        lecture['categories'].append( category.category_type )

    # Add the Poster image for this lecture's course
    lecture['SDPosterUrl'] = l.course.course_poster_url

    # Send the JSON response
    return http.HttpResponse(json.dumps(lecture), 
                             mimetype='application/json')

#   method: search
#   params: search_value
# response: A JSON Array of Course objects that match the search value.
#    notes: Search looks through the Course titles, categories, and course number.
#
def search(request, search_value):

    # Search through the Django Course objects using filters.
    matched_courses = Course.objects.filter( 
                      Q(title__icontains = search_value) |
                      Q(categories__category_type__icontains = search_value) |
                      Q(number__icontains = search_value)
                      ).distinct()

    course_list = []
    
    # build up a courses array, very similar to the courses array in the 
    # category_details method
    for course in matched_courses:
        course_info = {}
        course_info['id'] = course.id
        course_info['title'] = course.title
        course_info['number'] = course.number
        course_info['description'] = course.description
        course_info['release_date'] = course.release_date.strftime("%m/%d/%y")
        course_info['url']   = ('http://' + request.get_host() + 
                                reverse('library.views.course_detail', 
                                args=(course.id,))
                               )
        course_info['SDPosterUrl'] = course.course_poster_url
        course_list.append(course_info)

    # send the JSON response
    return http.HttpResponse(json.dumps(course_list), 
                             mimetype='application/json')
