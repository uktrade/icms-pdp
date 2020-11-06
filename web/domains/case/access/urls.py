from django.urls import path

from . import views


app_name = "access"
urlpatterns = [
    path("importer/request/", views.importer_access_request, name="importer-request"),
    path("exporter/request/", views.exporter_access_request, name="exporter-request"),
    # FIXME: makes reverse to crash
    # path("approval/", views.AccessRequestReviewView.as_view(), "approval"),
    path("requested/", views.AccessRequestCreatedView.as_view(), name="requested"),
]
