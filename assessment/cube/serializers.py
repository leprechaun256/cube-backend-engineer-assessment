from rest_framework import serializers
from cube.models import EndUserEvent


class EndUserEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = EndUserEvent
        fields = ['id', 'user', 'ts_source', 'timestamp', 'properties', 'noun', 'verb', 'time_spent']