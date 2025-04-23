from rest_framework import viewsets
from .models import Estudio
from .serializer import EstudioSerializer


class EstudioViewSet(viewsets.ModelViewSet):
    """
    CRUD de estudios sin autenticación.
    El cliente debe mandar:
        • folio          (str)
        • doctor         (ID)
        • paciente       (ID)
        • dicom_file     (archivo .dcm, multipart/form‑data)
    """
    queryset = Estudio.objects.all().select_related("paciente")
    serializer_class = EstudioSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        paciente_id = self.request.query_params.get("paciente")
        if paciente_id:
            qs = qs.filter(paciente_id=paciente_id)
        return qs
