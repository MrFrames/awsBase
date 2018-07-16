from django.contrib import admin
from .models import pastData, section, meetUp, post, place, type,\
    resolved_coord, capped_resolved_coord

# Register your models here.

admin.site.register(pastData)
admin.site.register(section)
admin.site.register(meetUp)
admin.site.register(post)
admin.site.register(place)
admin.site.register(type)
admin.site.register(resolved_coord)
admin.site.register(capped_resolved_coord)