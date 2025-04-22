from django.db import models

# Create your models here.


class Doctor(models.Model):
    nombre = models.CharField(max_length=120)
    apellido = models.CharField(max_length=120)

    class Meta:
        verbose_name = "doctor"
        verbose_name_plural = "doctores"
        ordering = ["apellido", "nombre"]
        indexes = [
            models.Index(fields=["apellido", "nombre"]),
        ]

    def __str__(self) -> str:
        return f"{self.apellido}, {self.nombre}"
