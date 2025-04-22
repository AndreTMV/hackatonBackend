from django.contrib import admin
from .models import Paciente

# Register your models here.


class PacienteAdmin(admin.ModelAdmin):
    list_display = ('curp', 'nombre', 'apellido',
                    'correo', 'telefono', 'edad', 'sexo')


admin.site.register(Paciente, PacienteAdmin)
