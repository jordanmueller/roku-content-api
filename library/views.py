from django import http
from datetime import datetime
from django.utils import simplejson as json
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.db.models import Q
from library.models import Category, Course, Lecture

def course_list(request):
    course_list = []

    for course in Course.objects.all():
        course_info = {}
        course_info['id'] = course.id
        course_info['title'] = course.title
        course_info['url']   = ('http://' + request.get_host() + 
                                reverse('library.views.course_detail', 
                                args=(course.id,))
                               )

        course_list.append(course_info)

    return http.HttpResponse(json.dumps(course_list), 
                             mimetype='application/json')


def course_detail(request, course_id):

    c = get_object_or_404(Course, pk=course_id)

    course = {}
    for key, value in c.__dict__.iteritems():
        if isinstance( value, unicode ):
            course[key] = value
        elif isinstance( value, int):
            course[key] = str(value)
        elif isinstance( value, datetime ):
            course[key] = value.strftime("%m/%d/%y")

    course['lectures'] = []

    for l in c.lecture_set.all():
        lecture = {}
        lecture['title'] = l.title
        lecture['id']    = l.id
        lecture['description'] = l.description
        lecture['url']   = ('http://' + request.get_host() + 
                            reverse('library.views.lecture_detail', 
                                    args=(c.id,l.id,))
                           )
        lecture['SDPosterUrl'] = 'http://' + request.get_host() + '/static/images/generic_course_sd.png'
        course['lectures'].append(lecture)

    return http.HttpResponse(json.dumps(course), 
                             mimetype='application/json')
    
def lecture_list(request, course_id):
    lecture_list = []

    for lecture in Lecture.objects.filter(course__id=course_id):
        lecture_info = {}

        lecture_info['id'] = lecture.id
        lecture_info['title'] = lecture.title
        lecture_info['url']   = ('http://' + request.get_host() + 
                                    reverse('library.views.lecture_detail', 
                                            args=(course_id,lecture.id,))
                                )

        lecture_list.append(lecture_info)

    return http.HttpResponse(json.dumps(lecture_list), 
                             mimetype='application/json')



def lecture_detail(request, course_id, lecture_id):
    l = get_object_or_404(Lecture, pk=lecture_id)

    lecture = {}
    for key, value in l.__dict__.iteritems():
        if isinstance( value, unicode ):
            lecture[key] = value
        elif isinstance( value, int):
            lecture[key] = str(value)
        elif isinstance( value, datetime ):
            lecture[key] = value.strftime("%m/%d/%y")

    lecture['course_title'] = l.course.title
    lecture['course_number'] = l.course.number

    lecture['categories'] = []
    for category in l.course.categories.all():
        lecture['categories'].append( category.category_type )

    lecture['SDPosterUrl'] = 'http://' + request.get_host() + '/static/images/generic_course_sd.png'

    return http.HttpResponse(json.dumps(lecture), 
                             mimetype='application/json')

def category_list(request):
    category_list = []

    for category in Category.objects.all():
        category_info = {}
        category_info['id'] = category.id
        category_info['name'] = category.category_type
        category_info['url']   = ('http://' + request.get_host() + 
                                    reverse('library.views.category_detail', 
                                            args=(category.id,))
                                )

        category_list.append(category_info)

    return http.HttpResponse(json.dumps(category_list), 
                             mimetype='application/json')

def category_detail(request, category_id):
    category = get_object_or_404(Category, pk=category_id)

    course_list = []
    
    for course in category.course_set.all():
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
        course_info['SDPosterUrl'] = 'http://' + request.get_host() + '/static/images/generic_course_sd.png'

        course_list.append(course_info)

    return http.HttpResponse(json.dumps(course_list), 
                             mimetype='application/json')

def search(request, search_value):

    matched_courses = Course.objects.filter( 
                      Q(title__icontains = search_value) |
                      Q(categories__category_type__icontains = search_value) |
                      Q(number__icontains = search_value)
                      ).distinct()

    course_list = []
    
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

        course_list.append(course_info)

    return http.HttpResponse(json.dumps(course_list), 
                             mimetype='application/json')
