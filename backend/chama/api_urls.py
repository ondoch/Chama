from django.urls import path
from rest_framework.routers import DefaultRouter

from .api_views import ChamaReportView, ChamaViewSet

router = DefaultRouter()
router.register("chamas", ChamaViewSet, basename="chama")

urlpatterns = [
    path("reports/chamas/", ChamaReportView.as_view(), name="chama-report"),
] + router.urls
