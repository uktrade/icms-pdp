from django.urls import path

from . import views


app_name = "access"
urlpatterns = [
    path("importer/", views.ImporterAccessRequestCreateView.as_view(), "importer"),
    path("exporter/", views.ExporterAccessRequestCreateView.as_view(), "exporter"),
    path("approval/", views.AccessRequestReviewView.as_view(), "approval"),
    path("requested/", views.AccessRequestCreatedView.as_view(), name="requested"),
]
