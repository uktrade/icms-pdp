from django.urls import include, path

from . import views

app_name = "fa-sil"

urlpatterns = [
    path("<int:application_pk>/edit/", views.edit, name="edit"),
    path("<int:pk>/submit/", views.submit, name="submit"),
    # Goods
    path("<int:pk>/sections/choose/", views.choose_goods_section, name="choose-goods-section"),
    path(
        "<int:application_pk>/<silsectiontype:sil_section_type>/",
        include(
            [
                path("add/", views.add_section, name="add-section"),
                path("<int:section_pk>/edit/", views.edit_section, name="edit-section"),
                path("<int:section_pk>/delete/", views.delete_section, name="delete-section"),
            ]
        ),
    ),
    # User section 5 authorities
    path(
        "<int:application_pk>/user-section5/",
        include(
            [
                path("add/", views.add_section5_document, name="add-section5-document"),
                path(
                    "<int:section5_pk>/archive/",
                    views.archive_section5_document,
                    name="archive-section5-document",
                ),
                path(
                    "<int:section5_pk>/view/",
                    views.view_section5_document,
                    name="view-section5-document",
                ),
            ]
        ),
    ),
    # Verified user section 5 authorities
    path(
        "<int:application_pk>/verified-section5/",
        include(
            [
                path(
                    "<int:section5_pk>/add/",
                    views.add_verified_section5,
                    name="add-verified-section5",
                ),
                path(
                    "<int:section5_pk>/delete/",
                    views.delete_verified_section5,
                    name="delete-verified-section5",
                ),
                path(
                    "<int:section5_pk>/view/",
                    views.view_verified_section5,
                    name="view-verified-section5",
                ),
                path(
                    "document/<int:document_pk>/view/",
                    views.view_verified_section5_document,
                    name="view-verified-section5-document",
                ),
            ]
        ),
    ),
]
