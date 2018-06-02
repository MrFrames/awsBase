from django.contrib import admin
from .models import pastData, section, meetUp, post, place, type

# Register your models here.

admin.site.register(pastData)
admin.site.register(section)
admin.site.register(meetUp)
admin.site.register(post)
admin.site.register(place)
admin.site.register(type)