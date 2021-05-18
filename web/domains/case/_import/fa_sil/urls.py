from django.urls import include, path

from . import views

app_name = "fa-sil"
urlpatterns = [
    path("<int:pk>/edit/", views.edit, name="edit"),
    # Goods
    path("<int:pk>/sections/choose/", views.choose_goods_section, name="choose-goods-section"),
    path(
        "<int:application_pk>/section1/",
        include(
            [
                path("add/", views.add_section1, name="add-section1"),
                path("<int:goods_pk>/edit/", views.edit_section1, name="edit-section1"),
                path("<int:goods_pk>/delete/", views.delete_section1, name="delete-section1"),
            ]
        ),
    ),
    path(
        "<int:application_pk>/section2/",
        include(
            [
                path("add/", views.add_section2, name="add-section2"),
                path("<int:goods_pk>/edit/", views.edit_section2, name="edit-section2"),
                path("<int:goods_pk>/delete/", views.delete_section2, name="delete-section2"),
            ]
        ),
    ),
    path(
        "<int:application_pk>/section5/",
        include(
            [
                path("add/", views.add_section5, name="add-section5"),
                path("<int:goods_pk>/edit/", views.edit_section5, name="edit-section5"),
                path("<int:goods_pk>/delete/", views.delete_section5, name="delete-section5"),
            ]
        ),
    ),
    path(
        "<int:application_pk>/section582-obsolete/",
        include(
            [
                path("add/", views.add_section582_obsolete, name="add-section582-obsolete"),
                path(
                    "<int:goods_pk>/edit/",
                    views.edit_section582_obsolete,
                    name="edit-section582-obsolete",
                ),
                path(
                    "<int:goods_pk>/delete/",
                    views.delete_section582_obsolete,
                    name="delete-section582-obsolete",
                ),
            ]
        ),
    ),
    path(
        "<int:application_pk>/section582-other/",
        include(
            [
                path("add/", views.add_section582_other, name="add-section582-other"),
                path(
                    "<int:goods_pk>/edit/",
                    views.edit_section582_other,
                    name="edit-section582-other",
                ),
                path(
                    "<int:goods_pk>/delete/",
                    views.delete_section582_other,
                    name="delete-section582-other",
                ),
            ]
        ),
    ),
]
