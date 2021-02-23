from django.urls import re_path

from . import views

urlpatterns = [
    re_path(
        "(?P<pk>[0-9]+)/edit",
        views.edit_sanctions_and_adhoc_licence_application,
        name="edit-sanctions-and-adhoc-licence-application",
    ),
    re_path(
        "validation-summary/(?P<pk>[0-9]+)/",
        views.sanctions_validation_summary,
        name="sanctions-validation-summary",
    ),
    re_path(
        "application-submit/(?P<pk>[0-9]+)/",
        views.sanctions_application_submit,
        name="sanctions-submit",
    ),
]
