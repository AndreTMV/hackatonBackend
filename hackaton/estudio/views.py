from rest_framework import viewsets, generics, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Estudio
from .serializer import EstudioSerializer, CargaEstudioSerializer
from .azure_dicom import list_series, list_instances

# ---------- sólo lectura ----------


class EstudioViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Estudio.objects.all().select_related("paciente")
    serializer_class = EstudioSerializer
    lookup_value_regex = r"[^/]+"
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        qs = super().get_queryset()
        pid = self.request.query_params.get("paciente")
        return qs.filter(paciente_id=pid) if pid else qs

    # --- QIDO ----
    @action(detail=True, methods=["get"])
    def series(self, request, pk=None):
        return Response(list_series(pk))

    @action(detail=True, methods=["get"],
            url_path=r"series/(?P<series_uid>[^/]+)/instances")
    def instances(self, request, pk=None, series_uid=None):
        return Response(list_instances(pk, series_uid))

# ---------- carga ----------


class CargaEstudioView(generics.CreateAPIView):
    serializer_class = CargaEstudioSerializer
    permission_classes = [permissions.AllowAny]
    lookup_value_regex = r"[^/]+"

    def get_serializer_context(self):
        # Reemplaza con tu función real que:
        # 1. copia `paths` al contenedor dicom-import/
        # 2. devuelve una SAS URL del folder
        return {"sas_url_func": lambda paths: "<sas_url_de_carpeta>"}
