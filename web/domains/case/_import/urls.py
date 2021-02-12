from django.urls import include, path, re_path

from . import views

app_name = "import"


urlpatterns = [
    path("", views.ImportApplicationChoiceView.as_view(), name="create"),
    path("create/sanctions/", views.create_sanctions, name="create-sanctions"),
    path("create/firearms/oil/", views.create_oil, name="create-oil"),
    path("sanctions/", include("web.domains.case._import.sanctions.urls")),
    path("firearms/", include("web.domains.case._import.firearms.urls")),

    # path("", views.ImportApplicationChoiceView.as_view(), name="new-import-application"),

    # Firearms and Ammunition - Open Individual Licence
    # path("firearms/oil/create/", views.create_oil, name="create-oil"),

    # path("firearms/oil/<int:pk>/edit/", views.edit_oil, name="edit-oil"),
    # path("firearms/oil/<int:pk>/validation/", views.validate_oil, name="oil-validation"),
    # path("firearms/oil/<int:pk>/submit/", views.submit_oil, name="submit-oil"),
    # Firearms and Ammunition - Management by ILB Admin


    ]



