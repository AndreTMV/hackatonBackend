from rest_framework import serializers
from .models import Estudio


class EstudioSerializer(serializers.ModelSerializer):
    url_descarga = serializers.SerializerMethodField()

    class Meta:
        model = Estudio
        fields = [
            "id", "folio",
            "paciente",
            "dicom_file", "fecha", "url_descarga",
        ]
        read_only_fields = ("id", "fecha", "url_descarga")

    def get_url_descarga(self, obj):
        return obj.url_descarga()
