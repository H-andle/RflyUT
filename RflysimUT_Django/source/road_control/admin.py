from django.contrib import admin

from source.road_control.models import RoadControl

@admin.register(RoadControl)
class RoadControlAdmin(admin.ModelAdmin):
    list_display = ['id', 'type', ]