from django.urls import path

from .api_views import OfficialViewSet

official_list = OfficialViewSet.as_view({"get": "list", "post": "create"})
official_detail = OfficialViewSet.as_view({"get": "retrieve", "delete": "destroy"})

urlpatterns = [
    path("chamas/<int:chama_pk>/officials/", official_list, name="chama-officials"),
    path("chamas/<int:chama_pk>/officials/<int:pk>/", official_detail, name="chama-official-detail"),
]
