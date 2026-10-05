from django.urls import path

from .api_views import AssignmentListView, AssignView, UnassignView

urlpatterns = [
    path("chamas/<int:chama_pk>/assign/", AssignView.as_view(), name="chama-assign"),
    path("chamas/<int:chama_pk>/unassign/", UnassignView.as_view(), name="chama-unassign"),
    path("chamas/<int:chama_pk>/assignments/", AssignmentListView.as_view(), name="chama-assignments"),
]
