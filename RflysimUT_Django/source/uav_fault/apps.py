from django.apps import AppConfig


class UavFaultConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'source.uav_fault'
    verbose_name = "故障注入"
