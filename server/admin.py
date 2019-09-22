from django.contrib import admin
from .models import Location, Course, Activity, Teacher, Teaching

admin.site.register(Location)
admin.site.register(Activity)
admin.site.register(Course)
admin.site.register(Teacher)
admin.site.register(Teaching)
