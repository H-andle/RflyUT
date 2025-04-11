from django.contrib import admin
from source.evaluation.models import Index, Values


@admin.register(Index)
class IndexAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', ]

@admin.register(Values)
class IndexAdmin(admin.ModelAdmin):
    list_display = ['id', 'index', 'value', ]
