from django.db import models
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator


class Paciente(models.Model):
    """
    Datos básicos de un paciente para el sistema DICOM.
    """

    curp = models.CharField(
        primary_key=True,
        max_length=18,
        unique=True,
        validators=[
            RegexValidator(
                regex=r"^[A-Z][AEIOUX][A-Z]{2}\d{2}(?:0[1-9]|1[0-2])"
                      r"(?:0[1-9]|[12]\d|3[01])[HM]"
                      r"(?:AS|BC|BS|CC|CS|CH|CL|CM|DF|DG|GT|GR|HG|JC|MC|MN|MS|NT|NL|OC|PL|QT|QR|SP|SL|SR|TC|TS|TL|VZ|YN|ZS)"
                      r"[B-DF-HJ-NP-TV-Z]{3}[A-Z\d]\d$",
                message="CURP inválida.",
            ),
        ],
        verbose_name="CURP",
        help_text="18 caracteres según el formato oficial de la CURP.",
    )

    nombre = models.CharField(max_length=120)
    apellido = models.CharField(max_length=120)

    correo = models.EmailField(unique=True)

    telefono = models.CharField(
        max_length=10,
        validators=[RegexValidator(
            r"^\d{10}$", message="Introduzca 10 dígitos.")],
        verbose_name="teléfono",
    )

    edad = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(0, "La edad no puede ser negativa."),
            MaxValueValidator(120, "La edad máxima permitida es 120 años."),
        ]
    )

    class Sexo(models.TextChoices):
        MASCULINO = "M", "Masculino"
        FEMENINO = "F", "Femenino"
        OTRO = "O", "Otro / No binario"
        NO_DECLARADO = "N", "No declarado"

    sexo = models.CharField(
        max_length=1,
        choices=Sexo.choices,
        default=Sexo.NO_DECLARADO,
    )

    class Meta:
        verbose_name = "paciente"
        verbose_name_plural = "pacientes"
        ordering = ["apellido", "nombre"]
        indexes = [
            models.Index(fields=["apellido", "nombre"]),
        ]

    def __str__(self) -> str:
        return f"{self.apellido}, {self.nombre} ({self.curp})"
