from django.urls import path
from rest_framework.routers import DefaultRouter

from .api_views import (
    AuditLogViewSet,
    CatalogView,
)


router = DefaultRouter()

router.register(
    r"audit-logs",
    AuditLogViewSet,
    basename="auditlog"
)


urlpatterns = [

    path(
        "catalog/",
        CatalogView.as_view(),
        name="catalog"
    ),

] + router.urls