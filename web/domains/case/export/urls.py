from django.urls import path

from . import views

app_name = "export"

urlpatterns = [
    path("create", views.ExportApplicationCreateView.as_view(), name="create"),
    path("com/<int:pk>/edit/", views.edit_com, name="com-edit"),
    path("com/<int:pk>/submit/", views.submit_com, name="com-submit"),
    path(
        "<int:pk>/case/take_ownership/", views.TakeOwnership.as_view(), name="case-take-ownership"
    ),
    path(
        "<int:pk>/case/release_ownership/",
        views.ReleaseOwnership.as_view(),
        name="case-release-ownership",
    ),
    path("<int:pk>/case/management/", views.Management.as_view(), name="case-management"),
    # TODO: add certificate of free sale URLs
]
