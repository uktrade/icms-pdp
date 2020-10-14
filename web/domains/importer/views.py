import structlog as logging
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.views.generic import View
from guardian.shortcuts import assign_perm, get_users_with_perms, remove_perm

from web.address.address import find as postcode_lookup
from web.company.companieshouse import api_get_companies
from web.domains.importer.forms import (
    AgentCreateIndividualForm,
    AgentEditIndividualForm,
    AgentOrganisationForm,
    ImporterFilter,
    ImporterIndividualDisplayForm,
    ImporterIndividualForm,
    ImporterOrganisationDisplayForm,
    ImporterOrganisationForm,
)
from web.domains.importer.models import Importer
from web.domains.office.forms import OfficeEditForm
from web.domains.user.forms import ContactForm
from web.domains.user.models import User
from web.views import ModelDetailView, ModelFilterView
from web.views.actions import Archive, CreateAgent, Edit, Unarchive

logger = logging.getLogger(__name__)


class ImporterListView(ModelFilterView):
    template_name = "web/domains/importer/list.html"
    filterset_class = ImporterFilter
    model = Importer
    queryset = Importer.objects.prefetch_related("offices").select_related("main_importer")
    page_title = "Maintain Importers"
    permission_required = "web.reference_data_access"

    class Display:
        fields = ["status", ("name", "user", "registered_number", "entity_type"), "offices"]
        fields_config = {
            "name": {"header": "Importer Name", "link": True,},
            "user": {"no_header": True, "link": True},
            "registered_number": {"header": "Importer Reg No",},
            "entity_type": {"header": "Importer Entity Type",},
            "status": {"header": "Status", "bold": True,},
            "offices": {"header": "Addresses", "show_all": True,},
        }
        opts = {"inline": True, "icon_only": True}
        actions = [Archive(**opts), Unarchive(**opts), CreateAgent(**opts), Edit(**opts)]


@login_required
@permission_required("web.reference_data_access", raise_exception=True)
def edit_importer(request, pk):
    importer = get_object_or_404(Importer, pk=pk)

    ImporterForm = ImporterIndividualForm
    if importer.is_organisation():
        ImporterForm = ImporterOrganisationForm

    if request.POST:
        form = ImporterForm(request.POST, instance=importer)
        if form.is_valid():
            form.save()
            return redirect(reverse("importer-edit", kwargs={"pk": pk}))
    else:
        form = ImporterForm(instance=importer)

    importer_contacts = get_users_with_perms(
        importer, only_with_perms_in=["is_contact_of_importer"]
    ).filter(user_permissions__codename="importer_access")
    available_contacts = User.objects.importer_access().exclude(pk__in=importer_contacts)

    context = {
        "object": importer,
        "form": form,
        "contact_form": ContactForm(available_contacts),
        "contacts": importer_contacts,
    }
    return render(request, "web/domains/importer/edit.html", context)


@login_required
@permission_required("web.reference_data_access", raise_exception=True)
def create_importer(request, entity):
    ImporterForm = ImporterIndividualForm
    if entity == "organisation":
        ImporterForm = ImporterOrganisationForm
    else:
        ImporterForm = ImporterIndividualForm

    if request.POST:
        form = ImporterForm(request.POST)
        if form.is_valid():
            importer = form.save()
            return redirect(reverse("importer-edit", kwargs={"pk": importer.pk}))
    else:
        form = ImporterForm()

    context = {
        "form": form,
    }

    return render(request, "web/domains/importer/create.html", context)


@login_required
@permission_required("web.reference_data_access", raise_exception=True)
@require_POST
def add_contact(request, pk):
    importer = get_object_or_404(Importer, pk=pk)

    available_contacts = User.objects.importer_access()
    form = ContactForm(available_contacts, request.POST)
    if form.is_valid():
        contact = form.cleaned_data["contact"]
        if importer.is_agent():
            permission = "web.is_agent_of_importer"
        else:
            permission = "web.is_contact_of_importer"
        assign_perm(permission, contact, importer)
    return redirect(reverse("importer-edit", kwargs={"pk": importer.pk}))


@login_required
@permission_required("web.reference_data_access", raise_exception=True)
@require_POST
def delete_contact(request, pk, contact_pk):
    importer = get_object_or_404(Importer, pk=pk)
    contact = get_object_or_404(User, pk=contact_pk)

    if importer.is_agent():
        permission = "web.is_agent_of_importer"
    else:
        permission = "web.is_contact_of_importer"
    remove_perm(permission, contact, importer)
    return redirect(reverse("importer-edit", kwargs={"pk": importer.pk}))


@login_required
@permission_required("web.reference_data_access", raise_exception=True)
def create_office(request, pk):
    importer = get_object_or_404(Importer, pk=pk)

    if request.POST:
        form = OfficeEditForm(request.POST)
        if form.is_valid():
            office = form.save()
            importer.offices.add(office)
            return redirect(reverse("importer-edit", kwargs={"pk": importer.pk}))
    else:
        form = OfficeEditForm()

    context = {"object": importer, "form": form}

    return render(request, "web/domains/importer/create-office.html", context)


@login_required
@permission_required("web.reference_data_access", raise_exception=True)
def edit_office(request, pk, office_pk):
    importer = get_object_or_404(Importer, pk=pk)
    office = get_object_or_404(importer.offices.filter(is_active=True), pk=office_pk)

    if request.POST:
        form = OfficeEditForm(request.POST, instance=office)
        if form.is_valid():
            form.save()
            return redirect(reverse("importer-edit", kwargs={"pk": importer.pk}))
    else:
        form = OfficeEditForm(instance=office)

    context = {
        "object": importer,
        "office": office,
        "form": form,
    }
    return render(request, "web/domains/importer/edit-office.html", context)


@login_required
@permission_required("web.reference_data_access", raise_exception=True)
@require_POST
def archive_office(request, pk, office_pk):
    importer = get_object_or_404(Importer, pk=pk)
    office = get_object_or_404(importer.offices.filter(is_active=True), pk=office_pk)
    office.is_active = False
    office.save()

    return redirect(reverse("importer-edit", kwargs={"pk": importer.pk}))


@login_required
@permission_required("web.reference_data_access", raise_exception=True)
@require_POST
def unarchive_office(request, pk, office_pk):
    importer = get_object_or_404(Importer, pk=pk)
    office = get_object_or_404(importer.offices.filter(is_active=False), pk=office_pk)
    office.is_active = True
    office.save()

    return redirect(reverse("importer-edit", kwargs={"pk": importer.pk}))


@login_required
@permission_required("web.reference_data_access", raise_exception=True)
def create_agent(request, importer_pk, entity):
    importer = get_object_or_404(Importer, pk=importer_pk)
    initial = {"main_importer": importer_pk}
    if entity == "organisation":
        AgentForm = AgentOrganisationForm
    else:
        AgentForm = AgentCreateIndividualForm

    if request.POST:
        form = AgentForm(request.POST, initial=initial)
        if form.is_valid():
            agent = form.save()
            return redirect(reverse("importer-agent-edit", kwargs={"pk": agent.pk}))
    else:
        form = AgentForm(initial=initial)

    context = {
        "object": importer,
        "form": form,
    }

    return render(request, "web/domains/importer/create-agent.html", context)


@login_required
@permission_required("web.reference_data_access", raise_exception=True)
def edit_agent(request, pk):
    agents = Importer.objects.filter(main_importer__isnull=False)
    agent = get_object_or_404(agents, pk=pk)

    if agent.is_organisation():
        AgentForm = AgentOrganisationForm
    else:
        AgentForm = AgentEditIndividualForm

    if request.POST:
        form = AgentForm(request.POST, instance=agent)
        if form.is_valid():
            form.save()
            return redirect(reverse("importer-agent-edit", kwargs={"pk": pk}))
    else:
        form = AgentForm(instance=agent)

    importer_contacts = get_users_with_perms(
        agent.main_importer, only_with_perms_in=["is_contact_of_importer"]
    ).filter(user_permissions__codename="importer_access")
    available_contacts = User.objects.importer_access().exclude(pk__in=importer_contacts)
    if agent.user:
        available_contacts = available_contacts.exclude(pk=agent.user.pk)

    context = {
        "object": agent.main_importer,
        "form": form,
        "contact_form": ContactForm(available_contacts),
        "contacts": importer_contacts,
    }
    return render(request, "web/domains/importer/edit-agent.html", context)


class AgentArchiveView(LoginRequiredMixin, PermissionRequiredMixin, View):
    queryset = Importer.objects.filter(main_importer__isnull=False)
    http_method_names = ["post"]
    permission_required = "web.reference_data_access"

    def post(self, request, *args, **kwargs):
        agent = get_object_or_404(self.queryset, pk=kwargs["pk"])
        agent.is_active = False
        agent.save()
        if not agent.is_organisation():
            remove_perm("web.is_agent_of_importer", agent.user, agent.main_importer)
        return redirect(reverse("importer-edit", kwargs={"pk": agent.main_importer.pk}))


class AgentUnArchiveView(LoginRequiredMixin, PermissionRequiredMixin, View):
    queryset = Importer.objects.filter(main_importer__isnull=False)
    http_method_names = ["post"]
    permission_required = "web.reference_data_access"

    def post(self, request, *args, **kwargs):
        agent = get_object_or_404(self.queryset, pk=kwargs["pk"])
        agent.is_active = True
        agent.save()
        if not agent.is_organisation():
            assign_perm("web.is_agent_of_importer", agent.user, agent.main_importer)
        return redirect(reverse("importer-edit", kwargs={"pk": agent.main_importer.pk}))


class ImporterOrganisationDetailView(ModelDetailView):
    template_name = "web/domains/importer/view.html"
    form_class = ImporterOrganisationDisplayForm
    model = Importer
    permission_required = "web.reference_data_access"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = ImporterOrganisationDisplayForm(instance=self.get_object())
        return context


class ImporterIndividualDetailView(ModelDetailView):
    template_name = "web/domains/importer/view.html"
    form_class = ImporterIndividualDisplayForm
    model = Importer
    permission_required = "web.reference_data_access"

    def get_context_data(self, object):
        context = super().get_context_data(object)

        form = ImporterIndividualDisplayForm(instance=object)
        user = object.user

        if user:
            form.initial["user_title"] = user.title
            form.initial["user_first_name"] = user.first_name
            form.initial["user_last_name"] = user.last_name
            form.initial["user_email"] = user.email
            form.initial["user_tel_no"] = "\n".join(
                f"{x.phone} ({x.entity_type})" for x in user.phone_numbers.all()
            )

        context["form"] = form

        return context


def importer_detail_view(request, pk):
    importer = Importer.objects.get(pk=pk)

    # there might be a better way to dynamically switch which view we're using
    # depending on the object type, but this works
    if importer.is_organisation():
        view = ImporterOrganisationDetailView.as_view()
    else:
        view = ImporterIndividualDetailView.as_view()

    return view(request, pk=pk)


def list_postcode_addresses(request,):
    postcode = request.POST.get("postcode")

    return JsonResponse(postcode_lookup(postcode), safe=False)


def list_companies(request):
    query = request.POST.get("query")
    companies = api_get_companies(query)

    return JsonResponse(companies, safe=False)
