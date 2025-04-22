from rest_framework import routers
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from doctor import views
from django.urls import path, include

router = routers.SimpleRouter()
router.register(r'doctor', views.DoctorView, 'doctor')

schema_view = get_schema_view(
    openapi.Info(
        title="Doctor API",
        default_version='v1',
        description="Doctor API documentation",
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
