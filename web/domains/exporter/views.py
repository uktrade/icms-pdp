from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_POST
from guardian.shortcuts import assign_perm, remove_perm

from web.domains.exporter.forms import AgentForm, ExporterFilter, ExporterForm
from web.domains.office.forms import OfficeForm
from web.domains.user.forms import ContactForm
from web.domains.user.models import User
from web.types import AuthenticatedHttpRequest
from web.views import ModelFilterView
from web.views.actions import Archive, CreateExporterAgent, Edit, Unarchive

from .models import Exporter
from .utils import available_contacts, exporter_contacts


class ExporterListView(ModelFilterView):
    template_name = "web/domains/exporter/list.html"
    filterset_class = ExporterFilter
    model = Exporter
    permission_required = "web.reference_data_access"
    page_title = "Maintain Exporters"

    class Display:
        fields = ["name", "offices", "agents"]
        fields_config = {
            "name": {"header": "Exporter Name", "link": True},
            "offices": {"header": "Addresses", "show_all": True},
            "agents": {"header": "Agent", "show_all": True},
        }
        opts = {"inline": True, "icon_only": True}
        actions = [Edit(**opts), CreateExporterAgent(**opts), Archive(**opts), Unarchive(**opts)]


@login_required
@permission_required("web.reference_data_access", raise_exception=True)
def edit_exporter(request: AuthenticatedHttpRequest, *, pk: int) -> HttpResponse:
    exporter = get_object_or_404(Exporter, pk=pk)

    if request.POST:
        form = ExporterForm(request.POST, instance=exporter)
        if form.is_valid():
            form.save()
            return redirect(reverse("exporter-edit", kwargs={"pk": pk}))
    else:
        form = ExporterForm(instance=exporter)

    contacts = available_contacts(exporter)
    context = {
        "object": exporter,
        "form": form,
        "contact_form": ContactForm(contacts),
        "contacts": exporter_contacts(exporter),
    }
    return render(request, "web/domains/exporter/edit.html", context)


@login_required
@permission_required("web.reference_data_access", raise_exception=True)
def detail_exporter(request: AuthenticatedHttpRequest, *, pk: int) -> HttpResponse:
    exporter = get_object_or_404(Exporter, pk=pk)

    context = {"object": exporter, "contacts": exporter_contacts(exporter)}

    return render(request, "web/domains/exporter/detail.html", context)


@login_required
@permission_required("web.reference_data_access", raise_exception=True)
def create_exporter(request: AuthenticatedHttpRequest, *, pk: int) -> HttpResponse:
    if request.POST:
        form = ExporterForm(request.POST)
        if form.is_valid():
            exporter = form.save()
            return redirect(reverse("exporter-edit", kwargs={"pk": exporter.pk}))
    else:
        form = ExporterForm()

    return render(request, "web/domains/exporter/create.html", {"form": form})


@login_required
@permission_required("web.reference_data_access", raise_exception=True)
@require_POST
def add_contact(request, pk):
    exporter = get_object_or_404(Exporter, pk=pk)

    contacts = available_contacts(exporter)
    form = ContactForm(contacts, request.POST)

    if form.is_valid():
        contact = form.cleaned_data["contact"]
        if exporter.is_agent():
            assign_perm("web.is_agent_of_exporter", contact, exporter.main_exporter)
            assign_perm("web.is_contact_of_exporter", contact, exporter)
        else:
            assign_perm("web.is_contact_of_exporter", contact, exporter)

    if exporter.is_agent():

        return redirect(reverse("exporter-agent-edit", kwargs={"pk": exporter.pk}))
    else:

        return redirect(reverse("exporter-edit", kwargs={"pk": exporter.pk}))


@login_required
@permission_required("web.reference_data_access", raise_exception=True)
@require_POST
def delete_contact(request: AuthenticatedHttpRequest, *, pk: int, contact_pk: int) -> HttpResponse:
    exporter = get_object_or_404(Exporter, pk=pk)
    contact = get_object_or_404(User, pk=contact_pk)

    if exporter.is_agent():
        remove_perm("web.is_agent_of_exporter", contact, exporter.main_exporter)
        remove_perm("web.is_contact_of_exporter", contact, exporter)

        return redirect(reverse("exporter-agent-edit", kwargs={"pk": exporter.pk}))
    else:
        remove_perm("web.is_contact_of_exporter", contact, exporter)

        return redirect(reverse("exporter-edit", kwargs={"pk": exporter.pk}))


@login_required
@permission_required("web.reference_data_access", raise_exception=True)
def create_office(request, pk):
    exporter = get_object_or_404(Exporter, pk=pk)

    if request.POST:
        form = OfficeForm(request.POST)
        if form.is_valid():
            office = form.save()
            exporter.offices.add(office)
            return redirect(
                reverse(
                    "exporter-office-edit",
                    kwargs={"exporter_pk": exporter.pk, "office_pk": office.pk},
                )
            )
    else:
        form = OfficeForm()

    context = {"object": exporter, "form": form}

    return render(request, "web/domains/exporter/create-office.html", context)


@login_required
@permission_required("web.reference_data_access", raise_exception=True)
def edit_office(request, exporter_pk, office_pk):
    exporter = get_object_or_404(Exporter, pk=exporter_pk)
    office = get_object_or_404(exporter.offices, pk=office_pk)

    if request.POST:
        form = OfficeForm(request.POST, instance=office)
        if form.is_valid():
            form.save()
    else:
        form = OfficeForm(instance=office)

    context = {
        "object": exporter,
        "office": office,
        "form": form,
    }
    return render(request, "web/domains/exporter/edit-office.html", context)


@login_required
@permission_required("web.reference_data_access", raise_exception=True)
@require_POST
def archive_office(request, exporter_pk, office_pk):
    exporter = get_object_or_404(Exporter, pk=exporter_pk)
    office = get_object_or_404(exporter.offices.filter(is_active=True), pk=office_pk)
    office.is_active = False
    office.save()

    return redirect(reverse("exporter-edit", kwargs={"pk": exporter.pk}))


@login_required
@permission_required("web.reference_data_access", raise_exception=True)
@require_POST
def unarchive_office(request, exporter_pk, office_pk):
    exporter = get_object_or_404(Exporter, pk=exporter_pk)
    office = get_object_or_404(exporter.offices.filter(is_active=False), pk=office_pk)
    office.is_active = True
    office.save()

    return redirect(reverse("exporter-edit", kwargs={"pk": exporter.pk}))


@login_required
@permission_required("web.reference_data_access", raise_exception=True)
def create_agent(request, exporter_pk):
    exporter = get_object_or_404(Exporter, pk=exporter_pk)
    initial = {"main_exporter": exporter_pk}

    if request.POST:
        form = AgentForm(request.POST, initial=initial)
        if form.is_valid():
            agent = form.save()
            # fixme: if ind set user as contact

            return redirect(reverse("exporter-agent-edit", kwargs={"pk": agent.pk}))
    else:
        form = AgentForm(initial=initial)

    context = {
        "object": exporter,
        "form": form,
    }

    return render(request, "web/domains/exporter/create-agent.html", context=context)


@login_required
@permission_required("web.reference_data_access", raise_exception=True)
def edit_agent(request, pk):
    agent = get_object_or_404(Exporter.objects.agents(), pk=pk)

    if request.POST:
        form = AgentForm(request.POST, instance=agent)
        if form.is_valid():
            agent = form.save()

            return redirect(reverse("exporter-agent-edit", kwargs={"pk": agent.pk}))
    else:
        form = AgentForm(instance=agent)

    contacts = available_contacts(agent)
    context = {
        "object": agent.main_exporter,
        "form": form,
        "contact_form": ContactForm(contacts),
        "contacts": exporter_contacts(agent),
    }

    return render(request, "web/domains/exporter/edit-agent.html", context=context)


@login_required
@permission_required("web.reference_data_access", raise_exception=True)
@require_POST
def archive_agent(self, pk):
    agent = get_object_or_404(Exporter.objects.agents().filter(is_active=True), pk=pk)
    agent.is_active = False
    agent.save()

    return redirect(reverse("exporter-edit", kwargs={"pk": agent.main_exporter.pk}))


@login_required
@permission_required("web.reference_data_access", raise_exception=True)
@require_POST
def unarchive_agent(self, pk):
    agent = get_object_or_404(Exporter.objects.agents().filter(is_active=False), pk=pk)
    agent.is_active = True
    agent.save()

    return redirect(reverse("exporter-edit", kwargs={"pk": agent.main_exporter.pk}))
