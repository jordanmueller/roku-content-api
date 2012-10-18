# urls.py is how the django application routes URL paths to the views.
# each line of the urls.py conf defines the behavior for a specific
# URL of the application.
#
# The first element in each tuple is a regular expression used to match the 
# path of a URL after the domain portion.  The first line in this config 
# matched a URL of the form www.sample.com/course.
#
# The second element in each tuple defines the method that will be called
# to build the server's response.  Each of these methods are in the library.views
# module.
#
# The ?P<param_name> assigns names to the parameters extracted within the 
# parenthesis of the regular expressions.

from django.conf.urls import patterns, url, include

urlpatterns = patterns('library.views',
    (r'^course/$', 'course_list' ),
    (r'^course/(?P<course_id>\d+)/$', 'course_detail' ),
    (r'^course/(?P<course_id>\d+)/lecture/$', 'lecture_list' ),
    (r'^course/(?P<course_id>\d+)/lecture/(?P<lecture_id>\d+)/$', 
        'lecture_detail' ),
    (r'^category/$', 'category_list' ),
    (r'^category/(?P<category_id>\d+)/$', 'category_detail' ),
    (r'^search/(?P<search_value>[\w .?\-",:]+)/$', 'search' ),
)
