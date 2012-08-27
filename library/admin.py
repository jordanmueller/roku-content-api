from library.models import Lecture, Course, Category
from django.contrib import admin

class CategoryAdmin(admin.ModelAdmin):
    pass

class LectureAdmin(admin.ModelAdmin):
    pass

class CourseAdmin(admin.ModelAdmin):
    pass

admin.site.register(Category, CategoryAdmin) 
admin.site.register(Lecture, LectureAdmin) 
admin.site.register(Course, CourseAdmin)

