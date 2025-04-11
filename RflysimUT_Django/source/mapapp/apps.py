# from rest_framework.views import APIView
# from rest_framework.response import Response
# from django.http import JsonResponse

from django.apps import AppConfig


class ExperimentConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'source.mapapp'
    verbose_name = "地图编辑"
