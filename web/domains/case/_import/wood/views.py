from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.forms.models import model_to_dict
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.utils import timezone
from django.views.decorators.http import require_GET, require_POST

from web.domains.case._import.models import ImportApplication
from web.domains.file.utils import create_file_model
from web.domains.template.models import Template
from web.flow.models import Task
from web.utils.validation import ApplicationErrors, PageErrors, create_page_errors

from .. import views as import_views
from .forms import (
    AddContractDocumentForm,
    EditContractDocumentForm,
    PrepareWoodQuotaForm,
    SubmitWoodQuotaForm,
    SupportingDocumentForm,
)
from .models import WoodQuotaApplication


@login_required
@permission_required("web.importer_access", raise_exception=True)
def edit_wood_quota(request, pk):
    with transaction.atomic():
        application = get_object_or_404(WoodQuotaApplication.objects.select_for_update(), pk=pk)

        task = application.get_task(ImportApplication.IN_PROGRESS, "prepare")

        if not request.user.has_perm("web.is_contact_of_importer", application.importer):
            raise PermissionDenied

        if request.POST:
            form = PrepareWoodQuotaForm(data=request.POST, instance=application)

            if form.is_valid():
                form.save()

                return redirect(reverse("import:wood:edit-quota", kwargs={"pk": pk}))

        else:
            form = PrepareWoodQuotaForm(instance=application, initial={"contact": request.user})

        supporting_documents = application.supporting_documents.filter(is_active=True)
        contract_documents = application.contract_documents.filter(is_active=True)

        context = {
            "process_template": "web/domains/case/import/partials/process.html",
            "process": application,
            "task": task,
            "form": form,
            "page_title": "Wood (Quota) Import Licence - Edit",
            "supporting_documents": supporting_documents,
            "contract_documents": contract_documents,
        }

        return render(request, "web/domains/case/import/wood/edit.html", context)


@login_required
@permission_required("web.importer_access", raise_exception=True)
def add_supporting_document(request, pk):
    with transaction.atomic():
        application = get_object_or_404(WoodQuotaApplication.objects.select_for_update(), pk=pk)

        task = application.get_task(ImportApplication.IN_PROGRESS, "prepare")

        if not request.user.has_perm("web.is_contact_of_importer", application.importer):
            raise PermissionDenied

        if request.POST:
            form = SupportingDocumentForm(data=request.POST, files=request.FILES)
            document = request.FILES.get("document")

            if form.is_valid():
                create_file_model(document, request.user, application.supporting_documents)

                return redirect(reverse("import:wood:edit-quota", kwargs={"pk": pk}))
        else:
            form = SupportingDocumentForm()

        context = {
            "process_template": "web/domains/case/import/partials/process.html",
            "process": application,
            "task": task,
            "form": form,
            "page_title": "Wood (Quota) Import Licence - Add supporting document",
        }

        return render(request, "web/domains/case/import/wood/add_supporting_document.html", context)


@require_GET
@login_required
def view_supporting_document(request, application_pk, document_pk):
    application = get_object_or_404(WoodQuotaApplication, pk=application_pk)

    return import_views.view_file(
        request, application, application.supporting_documents, document_pk
    )


@require_POST
@login_required
@permission_required("web.importer_access", raise_exception=True)
def delete_supporting_document(request, application_pk, document_pk):
    with transaction.atomic():
        application = get_object_or_404(
            WoodQuotaApplication.objects.select_for_update(), pk=application_pk
        )

        application.get_task(ImportApplication.IN_PROGRESS, "prepare")

        if not request.user.has_perm("web.is_contact_of_importer", application.importer):
            raise PermissionDenied

        document = application.supporting_documents.get(pk=document_pk)
        document.is_active = False
        document.save()

        return redirect(reverse("import:wood:edit-quota", kwargs={"pk": application_pk}))


@login_required
@permission_required("web.importer_access", raise_exception=True)
def add_contract_document(request, pk):
    with transaction.atomic():
        application = get_object_or_404(WoodQuotaApplication.objects.select_for_update(), pk=pk)

        task = application.get_task(ImportApplication.IN_PROGRESS, "prepare")

        if not request.user.has_perm("web.is_contact_of_importer", application.importer):
            raise PermissionDenied

        if request.POST:
            form = AddContractDocumentForm(data=request.POST, files=request.FILES)
            document = request.FILES.get("document")

            if form.is_valid():
                create_file_model(
                    document,
                    request.user,
                    application.contract_documents,
                    extra_args={
                        "reference": form.cleaned_data["reference"],
                        "contract_date": form.cleaned_data["contract_date"],
                    },
                )

                return redirect(reverse("import:wood:edit-quota", kwargs={"pk": pk}))
        else:
            form = AddContractDocumentForm()

        context = {
            "process_template": "web/domains/case/import/partials/process.html",
            "process": application,
            "task": task,
            "form": form,
            "page_title": "Wood (Quota) Import Licence - Add contract document",
        }

        return render(request, "web/domains/case/import/wood/add_contract_document.html", context)


@require_GET
@login_required
def view_contract_document(request, application_pk, document_pk):
    application = get_object_or_404(WoodQuotaApplication, pk=application_pk)

    return import_views.view_file(request, application, application.contract_documents, document_pk)


@require_POST
@login_required
@permission_required("web.importer_access", raise_exception=True)
def delete_contract_document(request, application_pk, document_pk):
    with transaction.atomic():
        application = get_object_or_404(
            WoodQuotaApplication.objects.select_for_update(), pk=application_pk
        )

        application.get_task(ImportApplication.IN_PROGRESS, "prepare")

        if not request.user.has_perm("web.is_contact_of_importer", application.importer):
            raise PermissionDenied

        document = application.contract_documents.get(pk=document_pk)
        document.is_active = False
        document.save()

        return redirect(reverse("import:wood:edit-quota", kwargs={"pk": application_pk}))


@login_required
@permission_required("web.importer_access", raise_exception=True)
def edit_contract_document(request, application_pk, document_pk):
    with transaction.atomic():
        application = get_object_or_404(
            WoodQuotaApplication.objects.select_for_update(), pk=application_pk
        )

        task = application.get_task(ImportApplication.IN_PROGRESS, "prepare")

        if not request.user.has_perm("web.is_contact_of_importer", application.importer):
            raise PermissionDenied

        document = application.contract_documents.get(pk=document_pk)

        if request.POST:
            form = EditContractDocumentForm(data=request.POST, instance=document)

            if form.is_valid():
                form.save()

                return redirect(reverse("import:wood:edit-quota", kwargs={"pk": application_pk}))

        else:
            form = EditContractDocumentForm(instance=document)

        context = {
            "process_template": "web/domains/case/import/partials/process.html",
            "process": application,
            "task": task,
            "form": form,
            "page_title": "Wood (Quota) Import Licence - Edit contract document",
        }

        return render(request, "web/domains/case/import/wood/edit_contract_document.html", context)


@login_required
@permission_required("web.importer_access", raise_exception=True)
def submit_wood_quota(request, pk: int) -> HttpResponse:
    with transaction.atomic():
        application = get_object_or_404(WoodQuotaApplication.objects.select_for_update(), pk=pk)

        task = application.get_task(ImportApplication.IN_PROGRESS, "prepare")

        if not request.user.has_perm("web.is_contact_of_importer", application.importer):
            raise PermissionDenied

        errors = ApplicationErrors()

        page_errors = PageErrors(
            page_name="Application details",
            url=reverse("import:wood:edit-quota", kwargs={"pk": pk}),
        )
        create_page_errors(
            PrepareWoodQuotaForm(data=model_to_dict(application), instance=application), page_errors
        )
        errors.add(page_errors)

        if request.POST:
            form = SubmitWoodQuotaForm(data=request.POST)

            if form.is_valid() and not errors.has_errors():
                application.status = ImportApplication.SUBMITTED
                application.submit_datetime = timezone.now()
                application.save()

                task.is_active = False
                task.finished = timezone.now()
                task.save()

                Task.objects.create(process=application, task_type="process", previous=task)

                return redirect(reverse("home"))

        else:
            form = SubmitWoodQuotaForm()

        declaration = Template.objects.filter(
            is_active=True,
            template_type=Template.DECLARATION,
            application_domain=Template.IMPORT_APPLICATION,
            template_code="IMA_WD_DECLARATION",
        ).first()

        context = {
            "process_template": "web/domains/case/import/partials/process.html",
            "process": application,
            "task": task,
            "form": form,
            "page_title": "Wood (Quota) Import Licence - Submit",
            "declaration": declaration,
            "errors": errors if errors.has_errors() else None,
        }

        return render(request, "web/domains/case/import/wood/submit.html", context)
