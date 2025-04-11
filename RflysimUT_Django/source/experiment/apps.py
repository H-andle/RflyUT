from django.apps import AppConfig


class ExperimentConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'source.experiment'
    verbose_name = "实验管理"