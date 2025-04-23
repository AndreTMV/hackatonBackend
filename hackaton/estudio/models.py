import uuid
from django.db import models
from django.utils import timezone

from paciente.models import Paciente
from .storage_backends import DicomAzureStorage


def dicom_upload_path(instance, filename):
    """
    Ruta dentro del contenedor:
    dicoms/2025/04/22/<UUID>.dcm
    """
    today = timezone.localdate()
    return f"{today:%Y/%m/%d}/{uuid.uuid4()}.dcm"


class Estudio(models.Model):
    """
    Un estudio DICOM subido por un doctor y
    asociado a un paciente.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    folio = models.CharField(max_length=30, unique=True)
    tipo = models.CharField(max_length=100)          # TC, RM, RX …

    paciente = models.ForeignKey(
        Paciente, on_delete=models.PROTECT, related_name="estudios")

    dicom_file = models.FileField(
        storage=DicomAzureStorage(),          # backend que creaste
        upload_to=dicom_upload_path
    )

    fecha = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ("-fecha",)
        indexes = [models.Index(fields=["paciente", "fecha"])]

    # — helpers —
    def __str__(self):
        return f"{self.folio} · {self.tipo} · {self.fecha:%Y‑%m‑%d}"

    def url_descarga(self):
        """URL SAS válida 15 min (generada por django‑storages)."""
        return self.dicom_file.url
