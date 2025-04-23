from django.db import models
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator


class Paciente(models.Model):
    """
    Datos básicos de un paciente para el sistema DICOM.
    """
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=120)
    fecha_nac = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name = "paciente"
        verbose_name_plural = "pacientes"
        ordering = ["nombre"]
        indexes = [
            models.Index(fields=["nombre"]),
        ]

    def __str__(self) -> str:
        return f"{self.nombre}"
