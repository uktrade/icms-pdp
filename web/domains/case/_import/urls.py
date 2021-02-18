from django.urls import include, path

from . import views

app_name = "import"

urlpatterns = [
    path("", views.ImportApplicationChoiceView.as_view(), name="choice"),
    path("create/sanctions/", views.create_sanctions, name="create-sanctions"),
    path("create/firearms/oil/", views.create_oil, name="create-oil"),
    path("create/wood/quota/", views.create_wood_quota, name="create-wood-quota"),
    # Applications
    path("sanctions/", include("web.domains.case._import.sanctions.urls")),
    path("firearms/", include("web.domains.case._import.firearms.urls")),
    path("wood/", include("web.domains.case._import.wood.urls")),
    # Importer case management
    path("case/<int:pk>/withdraw/", views.withdraw_case, name="withdraw-case"),
    path(
        "case/<int:application_pk>/withdraw/<int:withdrawal_pk>/archive/",
        views.archive_withdrawal,
        name="archive-withdrawal",
    ),
    # ILB Admin Case management
    path(
        "case/<int:pk>/take_ownership/",
        views.take_ownership,
        name="take-ownership",
    ),
    path(
        "case/<int:pk>/release_ownership/",
        views.release_ownership,
        name="release-ownership",
    ),
    path("case/<int:pk>/management/", views.manage_case, name="case-management"),
    # Common to Importer/ILB Admin
    path("case/<int:pk>/view/", views.view_case, name="view-case"),
]
