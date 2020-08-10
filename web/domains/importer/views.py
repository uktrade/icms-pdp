import structlog as logging
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.http import JsonResponse

from web.auth import utils as auth_utils

from web.domains.team.mixins import ContactsManagementMixin
from web.views import ModelCreateView, ModelDetailView, ModelFilterView, ModelUpdateView
from web.views.actions import Archive, Edit, Unarchive, CreateAgent

from .forms import (
    ImporterOrganisationDisplayForm,
    ImporterOrganisationEditForm,
    ImporterOrganisationForm,
    ImporterIndividualEditForm,
    ImporterIndividualDisplayForm,
    ImporterIndividualForm,
    ImporterFilter,
)
from .models import Importer

from web.domains.office.models import Office
from web.domains.office.forms import OfficeEditForm, OfficeFormSet

from django.forms import formset_factory

from web.address.address import find as postcode_lookup
from web.company.hmrc import api

logger = logging.getLogger(__name__)

permissions = ["IMP_MAINTAIN_ALL", "IMP_EDIT_SECTION5_AUTHORITY", "IMP_EDIT_FIREARMS_AUTHORITY"]


def has_permission(user):
    return auth_utils.has_any_permission(user, permissions)


class ImporterListView(ModelFilterView):
    template_name = "web/domains/importer/list.html"
    filterset_class = ImporterFilter
    model = Importer
    queryset = Importer.objects.prefetch_related("offices").select_related("main_importer")
    page_title = "Maintain Importers"

    def has_permission(self):
        return has_permission(self.request.user)

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


class ImporterEditView(ContactsManagementMixin, ModelUpdateView):
    template_name = "web/domains/importer/edit.html"
    success_url = reverse_lazy("importer-list")
    cancel_url = success_url
    model = Importer

    def has_permission(self):
        return has_permission(self.request.user)

    def get_form_class(self):
        importer = self.get_object()
        if importer.is_organisation():
            return ImporterOrganisationEditForm
        return ImporterIndividualEditForm

    def get(self, request, pk, offices_form=None, form=None):
        # should the offices formset be shown on the edit page
        # if we received the form, then we displayed as we want to
        # show the form and errors, otherwise
        show_offices_form = True
        if not offices_form:
            Formset = formset_factory(OfficeEditForm)
            offices_form = Formset()
            show_offices_form = False
        contact_context_data = super().get(request).context_data
        if self.extra_context is not None:
            contact_context_data.update(self.extra_context)

        return render(
            request,
            self.template_name,
            {
                "offices_form": offices_form,
                "success_url": self.success_url,
                "cancel_url": self.cancel_url,
                "view": self,
                "show_offices_form": show_offices_form,
                **contact_context_data,
            },
        )

    def add_people(self, *args, **kwargs):
        template_response = super().add_people(*args, **kwargs)
        self.extra_context = template_response.context_data
        return self.get(*args, **kwargs)

    def edit(self, request, pk):
        Formset = formset_factory(OfficeEditForm, formset=OfficeFormSet)
        offices_form = Formset(request.POST)

        form_class = self.get_form_class()
        form = form_class(request.POST, instance=self.get_object())

        if not offices_form.is_valid() or not form.is_valid():
            return self.get(request, pk, offices_form=offices_form)

        importer = form.save()

        for form in offices_form:
            office = form.save()
            importer.offices.add(office)
        super().save(request=request)

        return redirect("importer-view", pk=pk)

    def do_archive(self, request, is_active):
        if "item" not in request.POST:
            raise NameError()

        office = Office.objects.get(pk=int(request.POST.get("item", 0)))

        if not office:
            raise IndexError()

        office.is_active = is_active
        office.save()

    def archive(self, request, pk):
        self.do_archive(request, False)
        return redirect("importer-edit", pk=pk)

    def unarchive(self, request, pk):
        self.do_archive(request, True)
        return redirect("importer-edit", pk=pk)


class ImporterCreateMixin:
    template_name = "web/domains/importer/create.html"
    success_url = reverse_lazy("importer-list")
    cancel_url = success_url
    model = Importer

    def has_permission(self):
        return has_permission(self.request.user)

    def get_context_data(self, *args, **kwargs):
        Formset = formset_factory(OfficeEditForm)
        offices_form = Formset()
        self.extra_context = self.extra_context or {}
        self.extra_context = {
            "offices": Office.objects.none(),
            "offices_form": self.extra_context.get("offices_form", offices_form),
            "show_offices_form": self.extra_context.get("offices_form", False),
        }
        return super().get_context_data(*args, **kwargs)

    def post(self, *args, **kwargs):
        Formset = formset_factory(OfficeEditForm, formset=OfficeFormSet, extra=1)
        offices_form = Formset(self.request.POST)

        form = self.get_form()
        if form.is_valid() and offices_form.is_valid():
            return self.form_valid(form, offices_form)
        return self.form_invalid(form, offices_form)

    def form_valid(self, form, offices_form):
        self.object = form.save()
        for form in offices_form:
            office = form.save()
            self.object.offices.add(office)
        self.object.save()
        return super().form_valid(form)

    def form_invalid(self, form, offices_form):
        # required for PageTitleMixin - need to investigate
        self.object = None
        self.extra_context = {}
        # if an office form is submitted make sure we include it back
        if len(offices_form) > 0:
            self.extra_context = {"offices_form": offices_form}
        return self.render_to_response(self.get_context_data(form=form))


class ImporterIndividualCreate(ImporterCreateMixin, ModelCreateView):
    form_class = ImporterIndividualForm
    page_title = "Create Importer for Individual"

    def has_permission(self):
        return has_permission(self.request.user)


class ImporterOrganisationCreate(ImporterCreateMixin, ModelCreateView):
    form_class = ImporterOrganisationForm
    page_title = "Create Importer for Organisation"

    def has_permission(self):
        return has_permission(self.request.user)


class ImporterOrganisationDetailView(ContactsManagementMixin, ModelDetailView):
    template_name = "web/domains/importer/view.html"
    form_class = ImporterOrganisationDisplayForm
    model = Importer

    def has_permission(self):
        return has_permission(self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = ImporterOrganisationDisplayForm(instance=self.get_object)
        return context

    # required by ContactsManagementMixin.get
    def get_form_class(self, *args, **kwargs):
        return self.form_class


class ImporterIndividualDetailView(ContactsManagementMixin, ModelDetailView):
    template_name = "web/domains/importer/view.html"
    form_class = ImporterIndividualDisplayForm
    model = Importer

    def has_permission(self):
        return has_permission(self.request.user)

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

    # required by ContactsManagementMixin.get
    def get_form_class(self, *args, **kwargs):
        return self.form_class


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
    companies = api(query)

    return JsonResponse(companies, safe=False)
