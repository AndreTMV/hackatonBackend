from rest_framework import serializers
from .models import Estudio
from .azure_dicom import stow_many, start_bulk_job
import tempfile
import pathlib
import shutil
from django.core.files.uploadedfile import UploadedFile

# ---------- lectura ----------


class EstudioSerializer(serializers.ModelSerializer):
    wado_url = serializers.SerializerMethodField()

    class Meta:
        model = Estudio
        fields = ("study_uid", "folio", "paciente", "fecha", "wado_url")
        read_only_fields = ("study_uid", "fecha", "wado_url")

    def get_wado_url(self, obj):
        return obj.wado_url()

# ---------- carga ----------


class CargaEstudioSerializer(serializers.Serializer):
    folio = serializers.CharField(max_length=30)
    paciente = serializers.PrimaryKeyRelatedField(
        queryset=Estudio._meta.get_field("paciente").remote_field.model.objects.all())
    archivos = serializers.ListField(child=serializers.FileField(),
                                     allow_empty=False, write_only=True)

    def create(self, data):
        folio = data["folio"]
        paciente = data["paciente"]
        archivos = data["archivos"]                       # list[UploadedFile]
        tmpdir = tempfile.mkdtemp(prefix="dicom_")

        try:
            paths = []
            # --- renombrar con patrón <folio>-dcm-XXXX.dcm ---------------
            for idx, f in enumerate(archivos, start=1):
                name = f"{folio}-dcm-{idx:04d}.dcm"
                dest = pathlib.Path(tmpdir) / name
                with open(dest, "wb+") as out:
                    for chunk in f.chunks():
                        out.write(chunk)
                paths.append(dest)
            # ----------------------------------------------------------------
            if len(paths) <= 100:
                study_uids = stow_many(paths)

                if not study_uids:
                    raise serializers.ValidationError(
                        "El servicio DICOM no devolvió StudyInstanceUID. "
                        "Probablemente los archivos ya existían o son inválidos."
                    )

            else:
                # Necesitas subir paths al contenedor dicom-import/
                # y devolver una SAS de carpeta con tu propia función:
                sas_url = self.context["sas_url_func"](paths)
                job_id = start_bulk_job(sas_url)
                raise serializers.ValidationError(
                    f"Bulk Import lanzado (Job {job_id}). Espera a que termine en Azure."
                )

            created = []
            for uid in set(study_uids):
                est, _ = Estudio.objects.update_or_create(
                    study_uid=uid,
                    defaults={"folio": folio, "paciente": paciente})
                created.append(est)

            # protección extra (por si acaso)
            if not created:
                raise serializers.ValidationError(
                    "No se crearon registros de Estudio en la BD."
                )
            return created[0]
        finally:
            shutil.rmtree(tmpdir, ignore_errors=True)
