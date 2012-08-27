from django.conf.urls import patterns, url, include

urlpatterns = patterns('library.views',
    (r'^course/$', 'course_list' ),
    (r'^course/(?P<course_id>\d+)/$', 'course_detail' ),
    (r'^course/(?P<course_id>\d+)/lecture/$', 'lecture_list' ),
    (r'^course/(?P<course_id>\d+)/lecture/(?P<lecture_id>\d+)/$', 
        'lecture_detail' ),
    (r'^category/$', 'category_list' ),
    (r'^category/(?P<category_id>\d+)/$', 'category_detail' ),
    (r'^search/(?P<search_value>[\w ]+)/$', 'search' ),
)
