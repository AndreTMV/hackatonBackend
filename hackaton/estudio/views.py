from requests import api
from rest_framework import viewsets, generics, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Estudio
from rest_framework.decorators import api_view, permission_classes
from .serializer import EstudioSerializer, CargaEstudioSerializer
from .azure_dicom import list_series, list_instances, wado_instance_url

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


@api_view(['GET'])
def get_all_instance_urls(request, study_uid: str):
    urls = []
    for serie in list_series(study_uid):
        series_uid = serie["0020000E"]["Value"][0]
        # list_instances devuelve dicts, así que extraemos el UID aquí:
        for inst in list_instances(study_uid, series_uid):
            sop_list = inst.get("00080018", {}).get("Value", [])
            if not sop_list:
                continue
            sop_uid = sop_list[0]
            urls.append(wado_instance_url(study_uid, series_uid, sop_uid))
    return Response(urls)
