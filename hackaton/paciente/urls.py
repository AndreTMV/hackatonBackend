from rest_framework import routers
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from paciente import views
from django.urls import path, include

router = routers.SimpleRouter()
router.register(r'paciente', views.PacienteView, 'paciente')

schema_view = get_schema_view(
    openapi.Info(
        title="Paciente API",
        default_version='v1',
        description="Paciente API documentation",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@users.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("api/v1/", include(router.urls)),
    path('docs/', schema_view.with_ui('swagger',
                                      cache_timeout=0), name='schema-swagger-ui'),
]
