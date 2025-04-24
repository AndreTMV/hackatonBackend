from django.contrib import admin
from .models import Estudio


class EstudioAdmin(admin.ModelAdmin):
    list_display = (
        "study_uid",
        "folio",
        "paciente",
        "fecha",
    )
    search_fields = ("folio", "paciente__nombre")


admin.site.register(Estudio, EstudioAdmin)
