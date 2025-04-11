from django.contrib import admin

# Register your models here.
from source.flight_plan.models import FlightRequirements


@admin.register(FlightRequirements)
class FlightRequirementsAdmin(admin.ModelAdmin):
    list_display = ['id', 'drone', ]
