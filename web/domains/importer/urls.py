#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.urls import include, path

from . import views


urlpatterns = [
    path("", views.ImporterListView.as_view(), name="importer-list"),
    path("<int:pk>/edit/", views.ImporterEditView.as_view(), name="importer-edit"),
    path(
        "new/",
        include(
            [
                path(
                    "individual/",
                    views.ImporterIndividualCreate.as_view(),
                    name="importer-new-individual",
                ),
                path(
                    "organisation/",
                    views.ImporterOrganisationCreate.as_view(),
                    name="importer-new-organisation",
                ),
            ]
        ),
    ),
    path("<int:pk>/", views.importer_detail_view, name="importer-view"),
    # Importer Agents
    path(
        "<int:importer_id>/agent/<int:pk>/edit",
        views.ImporterEditView.as_view(),
        name="importer-agent-edit",
    ),
    path(
        "<int:pk>/agent/new/",
        include("web.domains.importer.urls_agent", namespace="importer-agent"),
    ),
    path("lookup/postcode", views.list_postcode_addresses, name="importer-postcode-lookup"),
    path("lookup/company", views.list_companies, name="importer-company-lookup"),
]
