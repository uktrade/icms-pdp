from django.urls import path

from web.domains.importer.views import AgentIndividualCreate, AgentOrganisationCreate


app_name = "agent"
urlpatterns = [
    path("individual/", AgentIndividualCreate.as_view(), name="create-individual",),
    path("organisation/", AgentOrganisationCreate.as_view(), name="create-organisation",),
]
