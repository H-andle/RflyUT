from django.apps import AppConfig


class FlightPlanConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'source.flight_plan'
    verbose_name = "飞行计划"
