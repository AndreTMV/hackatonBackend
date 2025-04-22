from django.contrib import admin
from .models import Estudio


class EstudioAdmin(admin.ModelAdmin):
    list_display = (
        "folio",
        "tipo",
        "doctor",
        "paciente",
        "fecha",
    )
    list_filter = ("tipo", "fecha", "doctor")
    search_fields = ("folio", "doctor__nombre", "paciente__nombre")


admin.site.register(Estudio, EstudioAdmin)
