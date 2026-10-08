from django.urls import path

from .api_views import AssignmentListView, AssignView, UnassignView

urlpatterns = [
    path("chamas/<uuid:public_id>/assign/", AssignView.as_view(), name="chama-assign"),
    path("chamas/<uuid:public_id>/unassign/", UnassignView.as_view(), name="chama-unassign"),
    path("chamas/<uuid:public_id>/assignments/", AssignmentListView.as_view(), name="chama-assignments"),
]
