from django.urls import path

from . import views

urlpatterns = [
    path(
        "<int:pk>/edit/",
        views.edit_sanctions_and_adhoc_licence_application,
        name="edit-sanctions-and-adhoc-licence-application",
    ),
    path(
        "<int:pk>/add-goods/",
        views.add_goods,
        name="add-goods",
    ),
    path(
        "<int:pk>/edit-goods/<int:goodspk>/",
        views.edit_goods,
        name="edit-goods",
    ),
    path(
        "validation-summary/<int:pk>/",
        views.sanctions_validation_summary,
        name="sanctions-validation-summary",
    ),
    path(
        "application-submit/<int:pk>/",
        views.sanctions_application_submit,
        name="sanctions-submit",
    ),
]
