from django.contrib import admin

from source.uav_fault.models import FaultPlans


@admin.register(FaultPlans)
class FaultPlansAdmin(admin.ModelAdmin):
    list_display = ['id', 'type', 'drone', ]
