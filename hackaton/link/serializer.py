# link/serializers.py
from rest_framework import serializers
from .models import EstudioLink


class EstudioLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstudioLink
        fields = ['id', 'estudio', 'doctor', 'vigencia', 'link']
        read_only_fields = ['vigencia', 'link']
