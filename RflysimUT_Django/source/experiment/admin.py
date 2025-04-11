from django.contrib import admin
from source.experiment.models import Experiments, EdgeLogs, FlightLogs
# Register your models here.
@admin.register(Experiments)
class ExperimentsAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', ]

@admin.register(FlightLogs)
class FlightLogsAdmin(admin.ModelAdmin):
    list_display = ['id', 'experiment', 'drone', ]

@admin.register(EdgeLogs)
class EdgeLogsAdmin(admin.ModelAdmin):
    list_display = ['id', 'experiment', 'edge', ]