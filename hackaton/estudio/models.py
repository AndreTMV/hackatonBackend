from django.db import models
from django.utils import timezone
from django.conf import settings
from paciente.models import Paciente


class Estudio(models.Model):
    """
    Referencia local a un Study almacenado en Azure DICOM Service.
    """
    study_uid = models.CharField(max_length=64, primary_key=True)
    folio = models.CharField(max_length=30, unique=True)
    paciente = models.ForeignKey(
        Paciente, on_delete=models.PROTECT, related_name="estudios")
    fecha = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ("-fecha",)
        indexes = [models.Index(fields=["paciente", "fecha"])]

    # --- helpers ---------------------------------------------------------
    def wado_url(self):
        base = settings.AZURE_DICOM_URL.rstrip("/")
        return f"{base}/v2/dicomweb/studies/{self.study_uid}"

    def __str__(self):
        return f"{self.folio} ({self.study_uid})"
