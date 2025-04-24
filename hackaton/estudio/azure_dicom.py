from __future__ import annotations
from django.conf import settings
from azure.identity import DefaultAzureCredential, ClientSecretCredential
import requests

"""Tiny SDK helper to work with Azure Health Data Services – DICOM service.

Usage patterns covered:
  • STOW‑RS upload for ≤ 100 instances
  • Bulk import from a folder in ADLS (SAS URI)
  • Basic QIDO‑RS queries (list series / list instances)
  • Utility to craft a WADO‑RS instance URL

The module auto‑caches AAD tokens for ~5 minutes to avoid hitting the
`/token` endpoint on every request.
"""

from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Iterable, Sequence
import json
import os
import re
from pathlib import Path
from typing import Sequence

_STUDY_RE = re.compile(r"/studies/([^/]+)/series")

###########################################################################
# 1. Authentication helpers
###########################################################################

_SCOPE = "https://dicom.healthcareapis.azure.com/.default"

_cred = (
    ClientSecretCredential(
        tenant_id=settings.AZURE_TENANT_ID,
        client_id=settings.AZURE_CLIENT_ID,
        client_secret=settings.AZURE_CLIENT_SECRET,
    )
    if getattr(settings, "AZURE_CLIENT_SECRET", None)
    else DefaultAzureCredential()
)

_cached_token: str | None = None
_expires_on: datetime | None = None


def _token() -> str:
    """Return a valid `Bearer <token>` string, refreshing if necessary."""
    global _cached_token, _expires_on

    if _cached_token and _expires_on and _expires_on - datetime.now(tz=timezone.utc) > timedelta(minutes=5):
        return _cached_token

    access_token = _cred.get_token(_SCOPE)
    _cached_token = f"Bearer {access_token.token}"
    _expires_on = datetime.fromtimestamp(
        access_token.expires_on, tz=timezone.utc)
    return _cached_token


###########################################################################
# 2. Base URLs – `AZURE_DICOM_URL` must be set in Django settings
###########################################################################

API_VERSION = os.getenv("AZURE_DICOM_API_VERSION", "v1")  # v1 or v2
_BASE = f"{settings.AZURE_DICOM_URL.rstrip('/')}/{API_VERSION}"


###########################################################################
# 3. Multipart builder for STOW‑RS
###########################################################################

def _multipart(paths: Iterable[Path]):
    """Build a *multipart/related* body compliant with DICOMweb STOW‑RS."""
    boundary = f"dicom_{os.urandom(8).hex()}"
    CRLF = b"\r\n"

    body_chunks: list[bytes] = []
    for p in paths:
        if not p.is_file():
            raise FileNotFoundError(p)
        body_chunks.extend([
            f"--{boundary}".encode(),
            b"Content-Type: application/dicom",
            f"Content-Location: {p.name}".encode(),
            b"",  # blank line
            p.read_bytes(),
        ])
    body_chunks.append(f"--{boundary}--".encode())

    body = CRLF.join(body_chunks)
    content_type = f"multipart/related; type=\"application/dicom\"; boundary={boundary}"
    return body, content_type


###########################################################################
# 4. STOW‑RS – upload ≤ 100 instances
###########################################################################

def stow_many(paths: Sequence[Path]) -> list[str]:
    """Upload up to 100 instances and return their StudyInstanceUIDs.

    The DICOMweb spec says the server only returns full metadata when the
    request includes ``Prefer: return=representation``.  Otherwise Azure
    will reply *202 Accepted* with a summary, which may be an empty JSON
    array.  We add that header and parse defensively.
    """
    if not paths:
        raise ValueError("paths cannot be empty")
    if len(paths) > 100:
        raise ValueError(
            "STOW-RS is limited to 100 instances; use bulk import instead")

    body, content_type = _multipart(paths)

    resp = requests.post(
        f"{_BASE}/studies",
        headers={
            "Authorization": _token(),
            "Content-Type": content_type,
            "Accept": "application/dicom+json",
            "Prefer": "return=representation",
        },
        data=body,
        timeout=300,
    )

    try:
        resp.raise_for_status()
    except requests.HTTPError as e:
        print("Status:", resp.status_code)
        print("Body :", resp.text)     # <-- aquí verás 00081197
        raise
    try:
        payload = resp.json()
        print(payload)
    except ValueError:
        # No JSON body (e.g. 202 with empty body)
        print("Vacio")
        return []

    # Payload can be an object or a list depending on server implementation
    payload_items = [payload] if isinstance(payload, dict) else payload

    uids: Set[str] = set()

    for item in payload_items:
        # ------------------------------------------
        # Caso A: el UID viene como (0020,000D)
        # ------------------------------------------
        tag_20_0d = item.get("0020000D", {})
        value = tag_20_0d.get("Value", [])
        if value:
            uids.add(value[0])
            # seguimos con el siguiente 'item'
            continue

        # ------------------------------------------
        # Caso B: buscar en la secuencia (0008,1199)
        # ------------------------------------------
        for seq_entry in item.get("00081199", {}).get("Value", []):
            url = seq_entry.get("00081190", {}).get("Value", [None])[0]
            if url:
                m = _STUDY_RE.search(url)
                if m:
                    uids.add(m.group(1))

        # (Opcional) también podrías revisar un 00081190 "suelo" en item
        # url = item.get("00081190", {}).get("Value", [None])[0]
        # ...

    print(uids)                 # quítalo en producción
    return list(uids)

###########################################################################
# 5. Bulk Import – more than 100 instances from ADLS
###########################################################################


def start_bulk_job(sas_url: str) -> str:
    payload = {
        "input": {
            "source": {"sasUri": sas_url},
            "storageType": "azureblob",
        }
    }
    resp = requests.post(
        f"{_BASE}/bulkimport/jobs?api-version=2023-03-01-dicom",
        headers={
            "Authorization": _token(),
            "Content-Type": "application/json",
        },
        json=payload,
        timeout=60,
    )
    resp.raise_for_status()
    return resp.json()["jobId"]


def bulk_job_status(job_id: str) -> dict:
    resp = requests.get(
        f"{_BASE}/bulkimport/jobs/{job_id}?api-version=2023-03-01-dicom",
        headers={"Authorization": _token()},
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()


###########################################################################
# 6. QIDO‑RS helpers
###########################################################################

def list_series(study_uid: str):
    resp = requests.get(
        f"{_BASE}/studies/{study_uid}/series",
        headers={
            "Authorization": _token(),
            "Accept": "application/dicom+json",
        },
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()


def list_instances(study_uid: str, series_uid: str):
    resp = requests.get(
        f"{_BASE}/studies/{study_uid}/series/{series_uid}/instances",
        headers={
            "Authorization": _token(),
            "Accept": "application/dicom+json",
        },
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()


###########################################################################
# 7. WADO‑RS helper
###########################################################################

def wado_instance_url(study_uid: str, series_uid: str, instance_uid: str) -> str:
    base = settings.AZURE_DICOM_URL.rstrip("/")
    return f"{base}/{API_VERSION}/studies/{study_uid}/series/{series_uid}/instances/{instance_uid}"
