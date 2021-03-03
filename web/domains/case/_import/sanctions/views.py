import structlog as logging
from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render, reverse

from web.domains.case._import.models import ImportApplication

from .forms import GoodsForm, SanctionsAndAdhocLicenseForm
from .models import SanctionsAndAdhocApplication, SanctionsAndAdhocApplicationGoods

logger = logging.getLogger(__name__)


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

        if request.method == "POST" and "delete" in request.POST.get("action", []):
            goods_pk = request.POST.get("item")
            SanctionsAndAdhocApplicationGoods.objects.get(pk=str(goods_pk)).delete()
            return redirect(
                reverse("import:edit-sanctions-and-adhoc-licence-application", kwargs={"pk": pk})
            )

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

        application_started = False
        if application.origin_country is not None and application.consignment_country is not None:
            application_started = True

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
            "application_started": application_started,
            "page_title": "Sanctions and Adhoc License Application",
        }
        return render(
            request,
            "web/domains/case/import/sanctions/add_or_edit_goods.html",
            context,
        )


@login_required
@permission_required("web.importer_access", raise_exception=True)
def edit_goods(request, pk, goodspk):
    with transaction.atomic():
        application = get_object_or_404(
            SanctionsAndAdhocApplication.objects.select_for_update(), pk=pk
        )
        task = application.get_task(ImportApplication.IN_PROGRESS, "prepare")

        if not request.user.has_perm("web.is_contact_of_importer", application.importer):
            raise PermissionDenied

        if request.method == "POST":
            form = GoodsForm(
                request.POST, instance=SanctionsAndAdhocApplicationGoods.objects.get(pk=goodspk)
            )
            if form.is_valid():
                obj = form.save(commit=False)
                obj.import_application = application
                obj.save()
                return redirect(
                    reverse(
                        "import:edit-sanctions-and-adhoc-licence-application", kwargs={"pk": pk}
                    )
                )
        else:
            form = GoodsForm(instance=SanctionsAndAdhocApplicationGoods.objects.get(pk=goodspk))

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
