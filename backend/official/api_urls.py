from django.urls import path

from .api_views import OfficialViewSet

official_list = OfficialViewSet.as_view({"get": "list", "post": "create"})
official_set = OfficialViewSet.as_view({"put": "replace_all"})
official_detail = OfficialViewSet.as_view({"get": "retrieve", "delete": "destroy"})

urlpatterns = [
    path("chamas/<str:chama_pk>/officials/", official_list, name="chama-officials"),
    path("chamas/<str:chama_pk>/officials/set/", official_set, name="chama-officials-set"),
    path("chamas/<str:chama_pk>/officials/<int:pk>/", official_detail, name="chama-official-detail"),
]
