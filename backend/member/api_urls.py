from django.urls import path

from .api_views import MemberViewSet

member_list = MemberViewSet.as_view({"get": "list", "post": "create"})
member_detail = MemberViewSet.as_view({"get": "retrieve", "put": "update", "patch": "partial_update",
                                       "delete": "destroy"})

urlpatterns = [
    path("chamas/<uuid:chama_public_id>/members/", member_list, name="chama-members"),
    path("chamas/<uuid:chama_public_id>/members/<int:pk>/", member_detail, name="chama-member-detail"),
]
