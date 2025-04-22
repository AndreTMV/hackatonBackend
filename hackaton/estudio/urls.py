from rest_framework.routers import DefaultRouter
from estudio.views import EstudioViewSet
from rest_framework import routers
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.urls import path, include


router = DefaultRouter()
router.register(r"estudios", EstudioViewSet, basename="estudio")

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
    path('docs/', schema_view.with_ui('swagger',
                                      cache_timeout=0), name='schema-swagger-ui'),
]
