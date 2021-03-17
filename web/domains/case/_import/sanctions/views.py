import structlog as logging
from django.conf import settings
from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.views.decorators.http import require_POST
from s3chunkuploader.file_handler import s3_client
from sentry_sdk import capture_exception

from web.domains.case._import.models import ImportApplication
from web.utils import FilevalidationService
from web.utils.s3upload import InvalidFileException, S3UploadService
from web.utils.virus import ClamAV, InfectedFileException

from .forms import DocumentForm, GoodsForm, SanctionsAndAdhocLicenseForm
from .models import SanctionsAndAdhocApplication, SanctionsAndAdhocApplicationGoods

logger = logging.getLogger(__name__)


def handle_uploaded_file(f, created_by, related_file_model):
    file_path = None
    error_message = None
    try:
        upload_service = S3UploadService(
            s3_client=s3_client(),
            virus_scanner=ClamAV(
                settings.CLAM_AV_USERNAME, settings.CLAM_AV_PASSWORD, settings.CLAM_AV_URL
            ),
            file_validator=FilevalidationService(),
        )

        file_path = upload_service.process_uploaded_file(settings.AWS_STORAGE_BUCKET_NAME, f)
    except (InvalidFileException, InfectedFileException) as e:
        error_message = str(e)
    except Exception as e:
        capture_exception(e)
        logger.exception(e)
        error_message = "Unknown error uploading file"
    finally:
        return related_file_model.create(
            filename=f.original_name,
            file_size=f.file_size,
            content_type=f.content_type,
            browser_content_type=f.content_type,
            error_message=error_message,
            path=file_path,
            created_by=created_by,
        )


@login_required
@permission_required("web.importer_access", raise_exception=True)
def edit_sanctions_and_adhoc_licence_application(request, pk):
    with transaction.atomic():
        application = get_object_or_404(
            SanctionsAndAdhocApplication.objects.select_for_update(), pk=pk
        )
        task = application.get_task(ImportApplication.IN_PROGRESS, "prepare")

        if not request.user.has_perm("web.is_contact_of_importer", application.importer):
            raise PermissionDenied

        application_started = False
        if application.origin_country is not None and application.consignment_country is not None:
            application_started = True

        if request.method == "POST":
            form = SanctionsAndAdhocLicenseForm(data=request.POST, instance=application)
            if form.is_valid():
                form.save()
                return redirect(
                    reverse(
                        "import:edit-sanctions-and-adhoc-licence-application", kwargs={"pk": pk}
                    )
                )
        else:
            form = SanctionsAndAdhocLicenseForm(
                instance=application, initial={"contact": request.user}
            )

        context = {
            "process_template": "web/domains/case/import/partials/process.html",
            "process": application,
            "task": task,
            "form": form,
            "application_started": application_started,
            "page_title": "Sanctions and Adhoc License Application",
            "goods_list": SanctionsAndAdhocApplicationGoods.objects.filter(
                import_application=application
            ),
        }
        return render(
            request,
            "web/domains/case/import/sanctions/edit_sanctions_and_adhoc_licence_application.html",
            context,
        )


@login_required
@permission_required("web.importer_access", raise_exception=True)
def add_goods(request, pk):
    with transaction.atomic():
        application = get_object_or_404(
            SanctionsAndAdhocApplication.objects.select_for_update(), pk=pk
        )
        task = application.get_task(ImportApplication.IN_PROGRESS, "prepare")

        if not request.user.has_perm("web.is_contact_of_importer", application.importer):
            raise PermissionDenied

        if request.method == "POST":
            goods_form = GoodsForm(request.POST)
            if goods_form.is_valid():
                obj = goods_form.save(commit=False)
                obj.import_application = application
                obj.save()
                return redirect(
                    reverse(
                        "import:edit-sanctions-and-adhoc-licence-application", kwargs={"pk": pk}
                    )
                )
        else:
            goods_form = GoodsForm()

        context = {
            "process_template": "web/domains/case/import/partials/process.html",
            "process": application,
            "task": task,
            "form": goods_form,
            "page_title": "Sanctions and Adhoc License Application",
        }
        return render(
            request,
            "web/domains/case/import/sanctions/add_or_edit_goods.html",
            context,
        )


@login_required
@permission_required("web.importer_access", raise_exception=True)
def edit_goods(request, application_pk, goods_pk):
    with transaction.atomic():
        application = get_object_or_404(
            SanctionsAndAdhocApplication.objects.select_for_update(), pk=application_pk
        )
        task = application.get_task(ImportApplication.IN_PROGRESS, "prepare")

        goods = get_object_or_404(application.sanctionsandadhocapplicationgoods_set, pk=goods_pk)

        if not request.user.has_perm("web.is_contact_of_importer", application.importer):
            raise PermissionDenied

        if request.method == "POST":
            form = GoodsForm(request.POST, instance=goods)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.import_application = application
                obj.save()
                return redirect(
                    reverse(
                        "import:edit-sanctions-and-adhoc-licence-application",
                        kwargs={"pk": application_pk},
                    )
                )
        else:
            form = GoodsForm(instance=goods)

        context = {
            "process_template": "web/domains/case/import/partials/process.html",
            "process": application,
            "task": task,
            "form": form,
            "page_title": "Sanctions and Adhoc License Application",
        }
        return render(
            request,
            "web/domains/case/import/sanctions/add_or_edit_goods.html",
            context,
        )


@login_required
@permission_required("web.importer_access", raise_exception=True)
@require_POST
def delete_goods(request, application_pk, goods_pk):
    with transaction.atomic():
        application = get_object_or_404(
            SanctionsAndAdhocApplication.objects.select_for_update(), pk=application_pk
        )
        if not request.user.has_perm("web.is_contact_of_importer", application.importer):
            raise PermissionDenied

        get_object_or_404(application.sanctionsandadhocapplicationgoods_set, pk=goods_pk).delete()

    return redirect(
        reverse(
            "import:edit-sanctions-and-adhoc-licence-application", kwargs={"pk": application_pk}
        )
    )


@login_required
@permission_required("web.importer_access", raise_exception=True)
def add_document(request, pk):
    with transaction.atomic():
        application = get_object_or_404(
            SanctionsAndAdhocApplication.objects.select_for_update(), pk=pk
        )
        task = application.get_task(ImportApplication.IN_PROGRESS, "prepare")

        if not request.user.has_perm("web.is_contact_of_importer", application.importer):
            raise PermissionDenied
        if request.method == "POST":
            documents_form = DocumentForm(request.POST, request.FILES)
            if documents_form.is_valid():

                files = request.FILES.getlist("files")
                for f in files:
                    handle_uploaded_file(f, request.user, files)

                obj = documents_form.save(commit=False)
                obj.import_application = application
                obj.save()
                return redirect(
                    reverse(
                        "import:edit-sanctions-and-adhoc-licence-application", kwargs={"pk": pk}
                    )
                )
        else:
            documents_form = DocumentForm()

        context = {
            "process_template": "web/domains/case/import/partials/process.html",
            "process": application,
            "task": task,
            "form": documents_form,
            "page_title": "Sanctions and Adhoc License Application",
        }
        return render(
            request,
            "web/domains/case/import/sanctions/add_document.html",
            context,
        )


@login_required
@permission_required("web.importer_access", raise_exception=True)
@require_POST
def delete_document(request, application_pk, goods_pk):
    with transaction.atomic():
        application = get_object_or_404(
            SanctionsAndAdhocApplication.objects.select_for_update(), pk=application_pk
        )
        if not request.user.has_perm("web.is_contact_of_importer", application.importer):
            raise PermissionDenied

        # get_object_or_404(application.sanctionsandadhocapplicationgoods_set, pk=goods_pk).delete()

    return redirect(
        reverse(
            "import:edit-sanctions-and-adhoc-licence-application", kwargs={"pk": application_pk}
        )
    )


@login_required
@permission_required("web.importer_access", raise_exception=True)
def sanctions_validation_summary(request, pk):
    with transaction.atomic():
        application = get_object_or_404(
            SanctionsAndAdhocApplication.objects.select_for_update(), pk=pk
        )
        task = application.get_task(ImportApplication.IN_PROGRESS, "prepare")

    context = {
        "process_template": "web/domains/case/import/partials/process.html",
        "process": application,
        "task": task,
        "application_title": "Sanctions and Adhoc License Application",
    }
    return render(
        request, "web/domains/case/import/sanctions/sanctions_validation_summary.html", context
    )


@login_required
@permission_required("web.importer_access", raise_exception=True)
def sanctions_application_submit(request, pk):
    with transaction.atomic():
        application = get_object_or_404(
            SanctionsAndAdhocApplication.objects.select_for_update(), pk=pk
        )
        task = application.get_task(ImportApplication.IN_PROGRESS, "prepare")

    context = {
        "process_template": "web/domains/case/import/partials/process.html",
        "process": application,
        "task": task,
        "application_title": "Sanctions and Adhoc License Application",
    }
    return render(
        request, "web/domains/case/import/sanctions/sanctions_application_submit.html", context
    )
