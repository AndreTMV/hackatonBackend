from drf_yasg import openapi
from django.urls import path, include
from rest_framework.routers import DefaultRouter, SimpleRouter
from .views import EstudioViewSet, CargaEstudioView, get_all_instance_urls
from drf_yasg.views import get_schema_view
from rest_framework import permissions

router = SimpleRouter()
router.register("estudios", EstudioViewSet, basename="estudio")

schema_view = get_schema_view(
    openapi.Info(
        title="Estudio API",
        default_version='v1',
        description="Estudio API documentation",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@users.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
urlpatterns = [
    path("api/v1/", include(router.urls)),
    path("api/v1/cargar-estudio/",
         CargaEstudioView.as_view(), name="cargar-estudio"),
    path(
        "api/v1/estudios/<str:study_uid>/all-instances/",
        view=get_all_instance_urls,
        name="estudio-all-instances"
    ),
]
