from django.contrib import admin
from source.proposal.models import Proposals, Modes, ProposalTypes


# Register your models here.
@admin.register(Proposals)
class ProposalsAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'mode', 'type' ]

@admin.register(Modes)
class ModestAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', ]

@admin.register(ProposalTypes)
class ProposalTypesAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', ]
