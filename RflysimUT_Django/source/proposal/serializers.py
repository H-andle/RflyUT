from rest_framework import serializers

from source.proposal.models import Modes, Proposals, ProposalTypes
from rest_framework.filters import BaseFilterBackend


class ModesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Modes
        fields = '__all__'

class ProposalsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proposals
        fields = '__all__'

class ProposalTypesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProposalTypes
        fields = '__all__'