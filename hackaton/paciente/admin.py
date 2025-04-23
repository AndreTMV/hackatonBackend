from django.contrib import admin
from .models import Paciente

# Register your models here.


class PacienteAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'fecha_nac')


admin.site.register(Paciente, PacienteAdmin)
