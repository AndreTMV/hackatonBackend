from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import EstudioLink
# o serializers si renombraste el archivo
from .serializer import EstudioLinkSerializer


class EstudioLinkViewSet(viewsets.ModelViewSet):
    """
    ViewSet para crear y obtener enlaces de estudio.
    GET /api/v1/links/          → lista todos los links
    POST /api/v1/links/         → crea un nuevo link
    GET /api/v1/links/{pk}/     → obtiene un link (410 si expiró)
    """
    queryset = EstudioLink.objects.all()
    serializer_class = EstudioLinkSerializer
    http_method_names = ['get', 'post', 'head',
                         'options']  # restringe solo a GET y POST

    def retrieve(self, request, *args, **kwargs):
        link = self.get_object()
        if link.is_expired():
            return Response({'detail': 'Link expirado'}, status=status.HTTP_410_GONE)
        return super().retrieve(request, *args, **kwargs)
