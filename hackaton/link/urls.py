from django.urls import path, include
from rest_framework import routers, permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from .views import EstudioLinkViewSet

router = routers.SimpleRouter()
router.register(r'links', EstudioLinkViewSet, basename='link')

schema_view = get_schema_view(
    openapi.Info(
        title="EstudioLink API",
        default_version='v1',
        description="Documentación de la API para generar y consultar enlaces de estudio",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="soporte@tu-dominio.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('api/v1/', include(router.urls)),
    path(
        'docs/',
        schema_view.with_ui('swagger', cache_timeout=0),
        name='schema-swagger-ui'
    ),
    path(
        'redoc/',
        schema_view.with_ui('redoc', cache_timeout=0),
        name='schema-redoc'
    ),
]
