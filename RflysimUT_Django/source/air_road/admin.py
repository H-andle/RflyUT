from django.contrib import admin
from source.air_road.models import Permissions, Layers, Nodes, Edges, Airports


# Register your models here.
@admin.register(Permissions)
class PermissionsAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', ]

@admin.register(Layers)
class LayerstAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'level', 'height']

@admin.register(Nodes)
class NodestAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', ]

@admin.register(Edges)
class EdgesAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', ]

@admin.register(Airports)
class AirportsAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', ]
