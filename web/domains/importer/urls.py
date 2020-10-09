from django.urls import path, re_path

from web.domains.importer import views

urlpatterns = [
    path("", views.ImporterListView.as_view(), name="importer-list"),
    path("<int:pk>/edit/", views.edit_importer, name="importer-edit"),
    re_path(
        "^(?P<entity>individual|organisation)/create/$",
        views.create_importer,
        name="importer-create",
    ),
    # contacts
    path("<int:pk>/", views.importer_detail_view, name="importer-view"),
    path("<int:pk>/contacts/add/", views.add_contact, name="importer-contact-add"),
    path(
        "<int:pk>/contacts/<int:contact_pk>/delete/",
        views.delete_contact,
        name="importer-contact-delete",
    ),
    # offices
    path("<int:pk>/offices/create/", views.create_office, name="importer-office-create"),
    path("<int:pk>/offices/<int:office_pk>/edit/", views.edit_office, name="importer-office-edit"),
    path(
        "<int:pk>/offices/<int:office_pk>/archive/",
        views.archive_office,
        name="importer-office-archive",
    ),
    path(
        "<int:pk>/offices/<int:office_pk>/unarchive/",
        views.unarchive_office,
        name="importer-office-unarchive",
    ),
    # Importer Agents
    path("agent/<int:pk>/edit/", views.edit_agent, name="importer-agent-edit",),
    path(
        "agent/<int:pk>/archive/", views.AgentArchiveView.as_view(), name="importer-agent-archive",
    ),
    path(
        "agent/<int:pk>/unarchive/",
        views.AgentUnArchiveView.as_view(),
        name="importer-agent-unarchive",
    ),
    re_path(
        "^(?P<importer_pk>[0-9]+)/agent/(?P<entity>individual|organisation)/create/$",
        views.create_agent,
        name="importer-agent-create",
    ),
    path("lookup/postcode", views.list_postcode_addresses, name="importer-postcode-lookup"),
    path("lookup/company", views.list_companies, name="importer-company-lookup"),
]
