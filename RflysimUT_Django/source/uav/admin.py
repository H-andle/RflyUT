from django.contrib import admin

from source.uav.models import Drones

@admin.register(Drones)
class DronesAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', ]
