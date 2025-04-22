# estudios/storage_backends.py
from django.conf import settings
from storages.backends.azure_storage import AzureStorage


class DicomAzureStorage(AzureStorage):
    """
    Backend de django‑storages que sube los DICOM al contenedor
    'dicoms' de la cuenta hackatondicoms y genera URL SAS temporales.
    """
    # — Credenciales (se inyectan desde settings / .env) —
    account_name = settings.AZURE_ACCOUNT_NAME          # hackatondicoms
    account_key = settings.AZURE_ACCOUNT_KEY           # la KEY1 / KEY2
    # ‑‑‑ Si usas cadena de conexión:
    # connection_string = settings.AZURE_CONNECTION_STRING

    # — Configuración de contenedor y SAS —
    azure_container = "dicoms"                             # contenedor privado
    expiration_secs = 60 * 15                              # 15 min
    overwrite_files = False                                # no sobrescribir blobs
    azure_ssl = True                                 # fuerza HTTPS
