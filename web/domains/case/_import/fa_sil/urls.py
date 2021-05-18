from django.urls import include, path

from . import views

app_name = "fa-sil"
urlpatterns = [
    path("<int:pk>/edit/", views.edit, name="edit"),
    # Goods
    path("<int:pk>/sections/choose/", views.choose_goods_section, name="choose-goods-section"),
    path(
        "<int:application_pk>/<silsectiontype:sil_section_type>/",
        include(
            [
                path("add/", views.add_goods, name="add-section"),
                path("<int:goods_pk>/edit/", views.edit_goods, name="edit-section"),
                path("<int:goods_pk>/delete/", views.delete_goods, name="delete-section"),
            ]
        ),
    ),
]
