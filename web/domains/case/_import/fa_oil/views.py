from django.conf import settings
from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.forms.models import model_to_dict
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_GET, require_POST

from web.domains.case._import.models import ImportApplication, ImportContact
from web.domains.file.utils import create_file_model
from web.domains.template.models import Template
from web.flow.models import Task
from web.notify import email
from web.utils.s3 import get_file_from_s3, get_s3_client
from web.utils.validation import (
    ApplicationErrors,
    FieldError,
    PageErrors,
    create_page_errors,
)

from .. import views as import_views
from .forms import (
    ChecklistFirearmsOILApplicationForm,
    ConstabularyEmailForm,
    ConstabularyEmailResponseForm,
    ImportContactLegalEntityForm,
    ImportContactPersonForm,
    PrepareOILForm,
    SubmitOILForm,
    UserImportCertificateForm,
)
from .models import (
    ConstabularyEmail,
    OpenIndividualLicenceApplication,
    UserImportCertificate,
    VerifiedCertificate,
)


@login_required
@permission_required("web.importer_access", raise_exception=True)
def edit_oil(request: HttpRequest, pk: int) -> HttpResponse:
    with transaction.atomic():
        application = get_object_or_404(
            OpenIndividualLicenceApplication.objects.select_for_update(), pk=pk
        )

        task = application.get_task(ImportApplication.IN_PROGRESS, "prepare")

        if not request.user.has_perm("web.is_contact_of_importer", application.importer):
            raise PermissionDenied

        if request.POST:
            form = PrepareOILForm(data=request.POST, instance=application)

            if form.is_valid():
                form.save()

                return redirect(reverse("import:fa-oil:edit-oil", kwargs={"pk": pk}))

        else:
            form = PrepareOILForm(instance=application, initial={"contact": request.user})

        context = {
            "process_template": "web/domains/case/import/partials/process.html",
            "process": application,
            "task": task,
            "form": form,
            "page_title": "Open Individual Import Licence - Edit",
        }

        return render(request, "web/domains/case/import/fa-oil/edit.html", context)


@login_required
@permission_required("web.importer_access", raise_exception=True)
def list_user_import_certificates(request: HttpRequest, pk: int) -> HttpResponse:
    with transaction.atomic():
        application = get_object_or_404(
            OpenIndividualLicenceApplication.objects.select_for_update(), pk=pk
        )

        task = application.get_task(ImportApplication.IN_PROGRESS, "prepare")

        if not request.user.has_perm("web.is_contact_of_importer", application.importer):
            raise PermissionDenied

        context = {
            "process_template": "web/domains/case/import/partials/process.html",
            "process": application,
            "task": task,
            "certificates": application.user_imported_certificates.active(),
            "verified_certificates": application.importer.firearms_authorities.active(),
            "page_title": "Open Individual Import Licence - Certificates",
        }

        return render(request, "web/domains/case/import/fa-oil/certificates/list.html", context)


@login_required
@permission_required("web.importer_access", raise_exception=True)
def create_user_import_certificate(request: HttpRequest, pk: int) -> HttpResponse:
    with transaction.atomic():
        application: OpenIndividualLicenceApplication = get_object_or_404(
            OpenIndividualLicenceApplication.objects.select_for_update(), pk=pk
        )

        task = application.get_task(ImportApplication.IN_PROGRESS, "prepare")

        if not request.user.has_perm("web.is_contact_of_importer", application.importer):
            raise PermissionDenied

        if request.POST:
            form = UserImportCertificateForm(data=request.POST, files=request.FILES)
            document = request.FILES.get("document")

            if form.is_valid():
                extra_args = {
                    field: value
                    for (field, value) in form.cleaned_data.items()
                    if field not in ["document"]
                }

                create_file_model(
                    document,
                    request.user,
                    application.user_imported_certificates,
                    extra_args=extra_args,
                )

                return redirect(
                    reverse("import:fa-oil:list-user-import-certificates", kwargs={"pk": pk})
                )
        else:
            form = UserImportCertificateForm()

        context = {
            "process_template": "web/domains/case/import/partials/process.html",
            "process": application,
            "task": task,
            "form": form,
            "page_title": "Open Individual Import Licence - Create Certificate",
        }

        return render(request, "web/domains/case/import/fa-oil/certificates/create.html", context)


@login_required
@permission_required("web.importer_access", raise_exception=True)
def edit_user_import_certificate(
    request: HttpRequest, application_pk: int, certificate_pk: int
) -> HttpResponse:
    with transaction.atomic():
        application = get_object_or_404(
            OpenIndividualLicenceApplication.objects.select_for_update(), pk=application_pk
        )
        certificate = get_object_or_404(UserImportCertificate, pk=certificate_pk)

        task = application.get_task(ImportApplication.IN_PROGRESS, "prepare")

        if not request.user.has_perm("web.is_contact_of_importer", application.importer):
            raise PermissionDenied

        if request.POST:
            form = UserImportCertificateForm(data=request.POST, instance=certificate)

            if form.is_valid():
                form.save()

                return redirect(
                    reverse(
                        "import:fa-oil:list-user-import-certificates",
                        kwargs={"pk": application_pk},
                    )
                )

        else:
            form = UserImportCertificateForm(instance=certificate)

        context = {
            "process_template": "web/domains/case/import/partials/process.html",
            "process": application,
            "task": task,
            "form": form,
            "page_title": f"Open Individual Import Licence - Edit Certificate '{certificate.reference}'",
            "certificate": certificate,
        }

        return render(request, "web/domains/case/import/fa-oil/certificates/edit.html", context)


@require_GET
@login_required
def view_user_import_certificate_file(
    request: HttpRequest, application_pk: int, certificate_pk: int
) -> HttpResponse:
    application: OpenIndividualLicenceApplication = get_object_or_404(
        OpenIndividualLicenceApplication, pk=application_pk
    )
    get_object_or_404(application.user_imported_certificates, pk=certificate_pk)

    return import_views.view_file(
        request, application, application.user_imported_certificates, certificate_pk
    )


@require_POST
@login_required
@permission_required("web.importer_access", raise_exception=True)
def delete_user_import_certificate(
    request: HttpRequest, application_pk: int, certificate_pk: int
) -> HttpResponse:
    with transaction.atomic():
        application: OpenIndividualLicenceApplication = get_object_or_404(
            OpenIndividualLicenceApplication.objects.select_for_update(), pk=application_pk
        )
        application.get_task(ImportApplication.IN_PROGRESS, "prepare")

        if not request.user.has_perm("web.is_contact_of_importer", application.importer):
            raise PermissionDenied

        document = application.user_imported_certificates.get(pk=certificate_pk)
        document.is_active = False
        document.save()

        return redirect(
            reverse("import:fa-oil:list-user-import-certificates", kwargs={"pk": application_pk})
        )


@login_required
@permission_required("web.importer_access", raise_exception=True)
def list_import_contacts(request, pk):
    with transaction.atomic():
        application = get_object_or_404(
            OpenIndividualLicenceApplication.objects.select_for_update(), pk=pk
        )

        task = application.get_task(ImportApplication.IN_PROGRESS, "prepare")

        if not request.user.has_perm("web.is_contact_of_importer", application.importer):
            raise PermissionDenied

        context = {
            "process_template": "web/domains/case/import/partials/process.html",
            "process": application,
            "task": task,
            "contacts": application.importcontact_set.all(),
            "page_title": "Open Individual Import Licence - Contacts",
        }

        return render(request, "web/domains/case/import/fa-oil/import-contacts/list.html", context)


@login_required
@permission_required("web.importer_access", raise_exception=True)
def create_import_contact(request, pk, entity):
    with transaction.atomic():
        application = get_object_or_404(
            OpenIndividualLicenceApplication.objects.select_for_update(), pk=pk
        )

        task = application.get_task(ImportApplication.IN_PROGRESS, "prepare")

        if not request.user.has_perm("web.is_contact_of_importer", application.importer):
            raise PermissionDenied

        if entity == ImportContact.LEGAL:
            Form = ImportContactLegalEntityForm
        else:
            Form = ImportContactPersonForm

        if request.POST:
            form = Form(data=request.POST, files=request.FILES)

            if form.is_valid():
                import_contact = form.save(commit=False)
                import_contact.import_application = application
                import_contact.entity = entity
                import_contact.save()

                # Assume known_bought_from is True if we are adding an import contact
                if not application.know_bought_from:
                    application.know_bought_from = True
                    application.save()

                return redirect(
                    reverse(
                        "import:fa-oil:edit-import-contact",
                        kwargs={
                            "application_pk": pk,
                            "entity": entity,
                            "contact_pk": import_contact.pk,
                        },
                    )
                )
        else:
            form = Form()

        context = {
            "process_template": "web/domains/case/import/partials/process.html",
            "process": application,
            "task": task,
            "form": form,
            "page_title": "Open Individual Import Licence",
        }

        return render(
            request, "web/domains/case/import/fa-oil/import-contacts/create.html", context
        )


@login_required
@permission_required("web.importer_access", raise_exception=True)
def edit_import_contact(request, application_pk, entity, contact_pk):
    with transaction.atomic():
        application = get_object_or_404(
            OpenIndividualLicenceApplication.objects.select_for_update(), pk=application_pk
        )
        person = get_object_or_404(ImportContact, pk=contact_pk)

        task = application.get_task(ImportApplication.IN_PROGRESS, "prepare")

        if not request.user.has_perm("web.is_contact_of_importer", application.importer):
            raise PermissionDenied

        if entity == ImportContact.LEGAL:
            Form = ImportContactLegalEntityForm
        else:
            Form = ImportContactPersonForm

        if request.POST:
            form = Form(data=request.POST, instance=person)

            if form.is_valid():
                form.save()

                return redirect(
                    reverse(
                        "import:fa-oil:edit-import-contact",
                        kwargs={
                            "application_pk": application_pk,
                            "entity": entity,
                            "contact_pk": contact_pk,
                        },
                    )
                )

        else:
            form = Form(instance=person)

        context = {
            "process_template": "web/domains/case/import/partials/process.html",
            "process": application,
            "task": task,
            "form": form,
            "page_title": "Open Individual Import Licence - Edit Import Contact",
        }

        return render(request, "web/domains/case/import/fa-oil/import-contacts/edit.html", context)


@login_required
@permission_required("web.importer_access", raise_exception=True)
def submit_oil(request: HttpRequest, pk: int) -> HttpResponse:
    with transaction.atomic():
        application = get_object_or_404(
            OpenIndividualLicenceApplication.objects.select_for_update(), pk=pk
        )

        task = application.get_task(ImportApplication.IN_PROGRESS, "prepare")

        if not request.user.has_perm("web.is_contact_of_importer", application.importer):
            raise PermissionDenied

        errors = ApplicationErrors()

        page_errors = PageErrors(
            page_name="Application details",
            url=reverse("import:fa-oil:edit-oil", kwargs={"pk": pk}),
        )
        create_page_errors(
            PrepareOILForm(data=model_to_dict(application), instance=application), page_errors
        )
        errors.add(page_errors)

        has_certificates = (
            application.user_imported_certificates.exists()
            or application.verified_certificates.exists()
        )

        if not has_certificates:
            page_errors = PageErrors(
                page_name="Certificates",
                url=reverse("import:fa-oil:list-user-import-certificates", kwargs={"pk": pk}),
            )

            page_errors.add(
                FieldError(
                    field_name="Certificate", messages=["At least one certificate must be added"]
                )
            )

            errors.add(page_errors)

        if application.know_bought_from and not application.importcontact_set.exists():
            page_errors = PageErrors(
                page_name="Details of who bought from",
                url=reverse("import:fa-oil:list-import-contacts", kwargs={"pk": pk}),
            )

            page_errors.add(
                FieldError(field_name="Person", messages=["At least one person must be added"])
            )

            errors.add(page_errors)

        if request.POST:
            form = SubmitOILForm(data=request.POST)

            if form.is_valid() and not errors.has_errors():
                application.status = ImportApplication.SUBMITTED
                application.submit_datetime = timezone.now()
                template = Template.objects.get(template_code="COVER_FIREARMS_OIL")
                application.cover_letter = template.get_content(
                    {
                        "CONTACT_NAME": application.contact,
                        "APPLICATION_SUBMITTED_DATE": application.submit_datetime,
                    }
                )
                application.save()

                # TODO: replace with Endorsement Usage Template (ICMSLST-638)
                endorsement = Template.objects.get(
                    is_active=True,
                    template_type=Template.ENDORSEMENT,
                    template_name="Open Individual Licence endorsement",
                )
                application.endorsements.create(content=endorsement.template_content)

                task.is_active = False
                task.finished = timezone.now()
                task.save()

                Task.objects.create(process=application, task_type="process", previous=task)

                return redirect(reverse("home"))

        else:
            form = SubmitOILForm()

        declaration = Template.objects.filter(
            is_active=True,
            template_type=Template.DECLARATION,
            application_domain=Template.IMPORT_APPLICATION,
            template_code="IMA_GEN_DECLARATION",
        ).first()

        context = {
            "process_template": "web/domains/case/import/partials/process.html",
            "process": application,
            "task": task,
            "page_title": "Open Individual Import Licence - Submit Application",
            "form": form,
            "declaration": declaration,
            "errors": errors if errors.has_errors() else None,
        }

        return render(request, "web/domains/case/import/fa-oil/submit.html", context)


@login_required
@permission_required("web.importer_access", raise_exception=True)
@require_POST
def toggle_verified_firearms(request, application_pk, authority_pk):
    with transaction.atomic():
        application = get_object_or_404(
            OpenIndividualLicenceApplication.objects.select_for_update(), pk=application_pk
        )
        firearms_authority = get_object_or_404(
            application.importer.firearms_authorities.active(), pk=authority_pk
        )

        application.get_task(ImportApplication.IN_PROGRESS, "prepare")

        if not request.user.has_perm("web.is_contact_of_importer", application.importer):
            raise PermissionDenied

        certificate, created = application.verified_certificates.get_or_create(
            firearms_authority=firearms_authority
        )
        if not created:
            certificate.delete()

        return redirect(
            reverse("import:fa-oil:list-user-import-certificates", kwargs={"pk": application_pk})
        )


@login_required
@permission_required("web.importer_access", raise_exception=True)
def view_verified_firearms(request, application_pk, authority_pk):
    with transaction.atomic():
        application = get_object_or_404(
            OpenIndividualLicenceApplication.objects.select_for_update(), pk=application_pk
        )
        firearms_authority = get_object_or_404(
            application.importer.firearms_authorities.active(), pk=authority_pk
        )

        task = application.get_task(ImportApplication.IN_PROGRESS, "prepare")

        if not request.user.has_perm("web.is_contact_of_importer", application.importer):
            raise PermissionDenied

        context = {
            "process_template": "web/domains/case/import/partials/process.html",
            "process": application,
            "task": task,
            "page_title": "Open Individual Import Licence - Verified Certificate",
            "firearms_authority": firearms_authority,
        }
        return render(
            request, "web/domains/case/import/fa-oil/certificates/view-verified.html", context
        )


@login_required
@permission_required("web.reference_data_access", raise_exception=True)
def manage_checklist(request, pk):
    with transaction.atomic():
        application = get_object_or_404(
            OpenIndividualLicenceApplication.objects.select_for_update(), pk=pk
        )
        task = application.get_task(ImportApplication.SUBMITTED, "process")
        checklist, _ = application.checklists.get_or_create()

        if request.POST:
            form = ChecklistFirearmsOILApplicationForm(request.POST, instance=checklist)
            if form.is_valid():
                form.save()
                return redirect(reverse("import:fa-oil:manage-checklist", kwargs={"pk": pk}))
        else:
            form = ChecklistFirearmsOILApplicationForm(instance=checklist)

        context = {
            "process": application,
            "task": task,
            "page_title": "Open Individual Import Licence - Checklist",
            "form": form,
        }

        return render(
            request=request,
            template_name="web/domains/case/import/management/checklist.html",
            context=context,
        )


@login_required
@permission_required("web.reference_data_access", raise_exception=True)
def manage_constabulary_emails(request, pk):
    with transaction.atomic():
        application = get_object_or_404(
            OpenIndividualLicenceApplication.objects.select_for_update(), pk=pk
        )
        task = application.get_task(ImportApplication.SUBMITTED, "process")

        context = {
            "process": application,
            "task": task,
            "page_title": "Constabulary Emails",
            "verified_certificates": application.verified_certificates.all(),
            "constabulary_emails": application.constabulary_emails.filter(is_active=True),
        }

        return render(
            request=request,
            template_name="web/domains/case/import/fa-oil/manage-constabulary-emails.html",
            context=context,
        )


@login_required
@permission_required("web.reference_data_access", raise_exception=True)
@require_POST
def create_constabulary_email(request, pk):
    with transaction.atomic():
        application = get_object_or_404(
            OpenIndividualLicenceApplication.objects.select_for_update(), pk=pk
        )
        application.get_task(ImportApplication.SUBMITTED, "process")
        template = Template.objects.get(is_active=True, template_code="IMA_CONSTAB_EMAIL")
        # TODO: replace with case reference
        goods_description = """Firearms, component parts thereof, or ammunition of any applicable
commodity code, other than those falling under Section 5 of the Firearms Act 1968 as amended."""
        body = template.get_content(
            {
                "CASE_REFERENCE": application.pk,
                "IMPORTER_NAME": application.importer.display_name,
                "IMPORTER_ADDRESS": application.importer_office,
                "GOODS_DESCRIPTION": goods_description,
                "CASE_OFFICER_NAME": request.user.full_name,
                "CASE_OFFICER_EMAIL": settings.ILB_CONTACT_EMAIL,
                "CASE_OFFICER_PHONE": settings.ILB_CONTACT_PHONE,
            }
        )
        constabulary_email = ConstabularyEmail.objects.create(
            application=application,
            status=ConstabularyEmail.DRAFT,
            email_subject=template.template_title,
            email_body=body,
            email_cc_address_list=settings.ICMS_FIREARMS_HOMEOFFICE_EMAIL,
        )

        return redirect(
            reverse(
                "import:fa-oil:edit-constabulary-email",
                kwargs={
                    "application_pk": application.pk,
                    "constabulary_email_pk": constabulary_email.pk,
                },
            )
        )


@login_required
@permission_required("web.reference_data_access", raise_exception=True)
def edit_constabulary_email(request, application_pk, constabulary_email_pk):
    with transaction.atomic():
        application = get_object_or_404(
            OpenIndividualLicenceApplication.objects.select_for_update(), pk=application_pk
        )
        task = application.get_task(ImportApplication.SUBMITTED, "process")
        constabulary_email = get_object_or_404(
            application.constabulary_emails.filter(is_active=True), pk=constabulary_email_pk
        )

        if request.POST:
            form = ConstabularyEmailForm(request.POST, instance=constabulary_email)
            if form.is_valid():
                constabulary_email = form.save()

                if "send" in request.POST:
                    attachments = []
                    s3_client = get_s3_client()

                    for document in constabulary_email.attachments.all():
                        file_content = get_file_from_s3(document.path, client=s3_client)
                        attachments.append((document.filename, file_content))

                    email.send_email(
                        constabulary_email.email_subject,
                        constabulary_email.email_body,
                        [constabulary_email.email_to],
                        constabulary_email.email_cc_address_list.split(","),
                        attachments,
                    )

                    constabulary_email.status = ConstabularyEmail.OPEN
                    constabulary_email.email_sent_datetime = timezone.now()
                    constabulary_email.save()

                    return redirect(
                        reverse(
                            "import:fa-oil:manage-constabulary-emails",
                            kwargs={
                                "pk": application_pk,
                            },
                        )
                    )

                return redirect(
                    reverse(
                        "import:fa-oil:edit-constabulary-email",
                        kwargs={
                            "application_pk": application_pk,
                            "constabulary_email_pk": constabulary_email_pk,
                        },
                    )
                )
        else:
            form = ConstabularyEmailForm(instance=constabulary_email)

        context = {
            "process": application,
            "task": task,
            "page_title": "Edit Constabulary Email",
            "form": form,
        }

        return render(
            request=request,
            template_name="web/domains/case/import/fa-oil/edit-constabulary-email.html",
            context=context,
        )


@login_required
@permission_required("web.reference_data_access", raise_exception=True)
@require_POST
def delete_constabulary_email(request, application_pk, constabulary_email_pk):
    with transaction.atomic():
        application = get_object_or_404(
            OpenIndividualLicenceApplication.objects.select_for_update(), pk=application_pk
        )
        application.get_task(ImportApplication.SUBMITTED, "process")
        constabulary_email = get_object_or_404(
            application.constabulary_emails.filter(is_active=True), pk=constabulary_email_pk
        )

        constabulary_email.is_active = False
        constabulary_email.save()

        return redirect(
            reverse(
                "import:fa-oil:manage-constabulary-emails",
                kwargs={
                    "pk": application_pk,
                },
            )
        )


@login_required
@permission_required("web.reference_data_access", raise_exception=True)
def add_response_constabulary_email(request, application_pk, constabulary_email_pk):
    with transaction.atomic():
        application = get_object_or_404(
            OpenIndividualLicenceApplication.objects.select_for_update(), pk=application_pk
        )
        task = application.get_task(ImportApplication.SUBMITTED, "process")
        constabulary_email = get_object_or_404(
            application.constabulary_emails, pk=constabulary_email_pk
        )

        if request.POST:
            form = ConstabularyEmailResponseForm(request.POST, instance=constabulary_email)
            if form.is_valid():
                constabulary_email = form.save(commit=False)
                constabulary_email.status = ConstabularyEmail.CLOSED
                constabulary_email.email_closed_datetime = timezone.now()
                constabulary_email.save()

                return redirect(
                    reverse(
                        "import:fa-oil:manage-constabulary-emails",
                        kwargs={
                            "pk": application_pk,
                        },
                    )
                )
        else:
            form = ConstabularyEmailResponseForm(instance=constabulary_email)

        context = {
            "process": application,
            "task": task,
            "page_title": "Add Response for Constabulary Email",
            "form": form,
            "object": constabulary_email,
        }

        return render(
            request=request,
            template_name="web/domains/case/import/fa-oil/add-response-constabulary-email.html",
            context=context,
        )


@require_GET
@login_required
def view_verified_certificate_file(request, application_pk, authority_pk, file_pk):
    application = get_object_or_404(OpenIndividualLicenceApplication, pk=application_pk)
    certificate = get_object_or_404(
        VerifiedCertificate, import_application=application, firearms_authority__pk=authority_pk
    )

    return import_views.view_file(
        request, application, certificate.firearms_authority.files, file_pk
    )