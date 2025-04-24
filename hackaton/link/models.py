from django.db import models

import uuid
from django.db import models
from django.utils import timezone
from django.conf import settings
from estudio.models import Estudio


class EstudioLink(models.Model):
    """
    Enlace temporal para acceder a un Estudio.
    """
    estudio = models.ForeignKey(
        Estudio, on_delete=models.CASCADE, related_name='links')
    doctor = models.BooleanField(default=False)
    vigencia = models.DateTimeField()
    link = models.URLField(max_length=200, unique=True)

    def save(self, *args, **kwargs):
        # Si no se definió vigencia, la ponemos 24 h a partir de ahora
        if not self.vigencia:
            self.vigencia = timezone.now() + timezone.timedelta(hours=24)
        # Si no se definió link, lo construimos según doctor/paciente
        if not self.link:
            base = getattr(settings, 'FRONTEND_URL',
                           'https://salud-digna-hackaton2025.vercel.app/').rstrip('/')
            ruta = 'Doctor' if self.doctor else 'paciente'
            # Usamos study_uid para armar la ruta
            self.link = f'{base}/{ruta}/{self.estudio.study_uid}'
        super().save(*args, **kwargs)

    def is_expired(self):
        return timezone.now() > self.vigencia

    def __str__(self):
        role = 'doctor' if self.doctor else 'paciente'
        return f'Link [{role}] → {self.estudio.study_uid}'
