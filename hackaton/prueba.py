from estudio.azure_dicom import list_series, list_instances, wado_instance_url


def get_all_instance_urls(study_uid: str) -> list[str]:
    urls = []
    for serie in list_series(study_uid):
        sid = serie["0020000E"]["Value"][0]           # SeriesInstanceUID
        for inst_uid in list_instances(study_uid, sid):  # SOPInstanceUID
            urls.append(wado_instance_url(study_uid, sid, inst_uid))
    return urls


# Uso:
study = "1.2.840.113845.13.36061.743028493.2593146950597"
all_urls = get_all_instance_urls(study)
