from django import admin
from django import mark_safe
from courses.models import *

class MyCourseAdmin(admin.ModelAdmin, admin.AdminSite):
    list_display = ["id", "name", "created_date", "updated_date", "active"]
    search_fields = ["name"]
    list_filter = ["name", "created_date"]
    readonly_fields = ["my_image"]
    form = CourseForm
    site_header = "Ecourse Admin Page"

    def my_image(self, course):
        if course.image:
            return mark_safe(f"<img src='/static/{course.image.name}' width='400'/>")

admin.site.register(Course, MyCourseAdmin)
admin.site.register(Category, MyCourseAdmin)
admin.site.register(Lesson)
admin.site.register(Tag)

# Register your models here.
