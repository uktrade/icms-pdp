from typing import Type, Union

from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.forms import ModelForm
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_POST

from ..models import ImportApplication
from . import forms, models

Goods = Union[
    models.SILGoodsSection1,
    models.SILGoodsSection2,
    models.SILGoodsSection5,
    models.SILGoodsSection582Obsolete,
    models.SILGoodsSection582Other,
]
GoodsT = Type[Goods]


@login_required
@permission_required("web.importer_access", raise_exception=True)
def edit(request: HttpRequest, pk: int) -> HttpResponse:
    with transaction.atomic():
        application = get_object_or_404(models.SILApplication.objects.select_for_update(), pk=pk)

        task = application.get_task(ImportApplication.IN_PROGRESS, "prepare")

        if not request.user.has_perm("web.is_contact_of_importer", application.importer):
            raise PermissionDenied

        if request.POST:
            form = forms.PrepareSILForm(data=request.POST, instance=application)

            if form.is_valid():
                form.save()

                return redirect(reverse("import:fa-sil:edit", kwargs={"pk": pk}))

        else:
            form = forms.PrepareSILForm(instance=application, initial={"contact": request.user})

        context = {
            "process_template": "web/domains/case/import/partials/process.html",
            "process": application,
            "task": task,
            "form": form,
            "page_title": "Firearms and Ammunition (Specific Import Licence) - Edit",
        }

        return render(request, "web/domains/case/import/fa-sil/edit.html", context)


@login_required
@permission_required("web.importer_access", raise_exception=True)
def choose_goods_section(request: HttpRequest, *, pk: int) -> HttpResponse:
    with transaction.atomic():
        application: models.SILApplication = get_object_or_404(
            models.SILApplication.objects.select_for_update(), pk=pk
        )

        task = application.get_task(ImportApplication.IN_PROGRESS, "prepare")

        if not request.user.has_perm("web.is_contact_of_importer", application.importer):
            raise PermissionDenied

        context = {
            "process_template": "web/domains/case/import/partials/process.html",
            "process": application,
            "task": task,
            "page_title": "Firearms and Ammunition (Specific Import Licence) - Edit Goods",
        }

        return render(request, "web/domains/case/import/fa-sil/choose-goods-section.html", context)


@login_required
@permission_required("web.importer_access", raise_exception=True)
def add_section1(request: HttpRequest, *, application_pk: int) -> HttpResponse:
    form_class = forms.SILGoodsSection1Form
    template = "web/domains/case/import/fa-sil/goods/section1.html"
    return _add_goods(request, application_pk, form_class, template)


@login_required
@permission_required("web.importer_access", raise_exception=True)
def add_section2(request: HttpRequest, *, application_pk: int) -> HttpResponse:
    form_class = forms.SILGoodsSection2Form
    template = "web/domains/case/import/fa-sil/goods/section2.html"
    return _add_goods(request, application_pk, form_class, template)


@login_required
@permission_required("web.importer_access", raise_exception=True)
def add_section5(request: HttpRequest, *, application_pk: int) -> HttpResponse:
    form_class = forms.SILGoodsSection5Form
    template = "web/domains/case/import/fa-sil/goods/section5.html"
    return _add_goods(request, application_pk, form_class, template)


@login_required
@permission_required("web.importer_access", raise_exception=True)
def add_section582_other(request: HttpRequest, *, application_pk: int) -> HttpResponse:
    form_class = forms.SILGoodsSection582Other
    template = "web/domains/case/import/fa-sil/goods/section582-other.html"
    return _add_goods(request, application_pk, form_class, template)


@login_required
@permission_required("web.importer_access", raise_exception=True)
def add_section582_obsolete(request: HttpRequest, *, application_pk: int) -> HttpResponse:
    form_class = forms.SILGoodsSection582ObsoleteForm
    template = "web/domains/case/import/fa-sil/goods/section582-obsolete.html"
    return _add_goods(request, application_pk, form_class, template)


def _add_goods(
    request: HttpRequest, application_pk: int, form_class: Type[ModelForm], template: str
) -> HttpResponse:
    with transaction.atomic():
        application: models.SILApplication = get_object_or_404(
            models.SILApplication.objects.select_for_update(), pk=application_pk
        )

        task = application.get_task(ImportApplication.IN_PROGRESS, "prepare")

        if not request.user.has_perm("web.is_contact_of_importer", application.importer):
            raise PermissionDenied

        if request.POST:
            form = form_class(request.POST)
            if form.is_valid():
                goods = form.save(commit=False)
                goods.import_application = application
                goods.save()
                return redirect(reverse("import:fa-sil:edit", kwargs={"pk": application.pk}))
        else:
            form = form_class()

        context = {
            "process_template": "web/domains/case/import/partials/process.html",
            "process": application,
            "task": task,
            "form": form,
            "page_title": "Firearms and Ammunition (Specific Import Licence) - Add Goods",
        }

        return render(request, template, context)


@login_required
@permission_required("web.importer_access", raise_exception=True)
def edit_section1(request: HttpRequest, *, application_pk: int, goods_pk: int) -> HttpResponse:
    goods_class = models.SILGoodsSection1
    form_class = forms.SILGoodsSection1Form
    template = "web/domains/case/import/fa-sil/goods/section1.html"
    return _edit_goods(request, application_pk, goods_pk, goods_class, form_class, template)


@login_required
@permission_required("web.importer_access", raise_exception=True)
def edit_section2(request: HttpRequest, *, application_pk: int, goods_pk: int) -> HttpResponse:
    goods_class = models.SILGoodsSection2
    form_class = forms.SILGoodsSection2Form
    template = "web/domains/case/import/fa-sil/goods/section2.html"
    return _edit_goods(request, application_pk, goods_pk, goods_class, form_class, template)


@login_required
@permission_required("web.importer_access", raise_exception=True)
def edit_section5(request: HttpRequest, *, application_pk: int, goods_pk: int) -> HttpResponse:
    goods_class = models.SILGoodsSection5
    form_class = forms.SILGoodsSection5Form
    template = "web/domains/case/import/fa-sil/goods/section5.html"
    return _edit_goods(request, application_pk, goods_pk, goods_class, form_class, template)


@login_required
@permission_required("web.importer_access", raise_exception=True)
def edit_section582_other(
    request: HttpRequest, *, application_pk: int, goods_pk: int
) -> HttpResponse:
    goods_class = models.SILGoodsSection582Other
    form_class = forms.SILGoodsSection582Other
    template = "web/domains/case/import/fa-sil/goods/section582-other.html"
    return _edit_goods(request, application_pk, goods_pk, goods_class, form_class, template)


@login_required
@permission_required("web.importer_access", raise_exception=True)
def edit_section582_obsolete(
    request: HttpRequest, *, application_pk: int, goods_pk: int
) -> HttpResponse:
    goods_class = models.SILGoodsSection582Other
    form_class = forms.SILGoodsSection582ObsoleteForm
    template = "web/domains/case/import/fa-sil/goods/section582-obsolete.html"
    return _edit_goods(request, application_pk, goods_pk, goods_class, form_class, template)


def _edit_goods(
    request: HttpRequest,
    application_pk: int,
    goods_pk: int,
    goods_class: GoodsT,
    form_class: Type[ModelForm],
    template: str,
) -> HttpResponse:
    with transaction.atomic():
        application: models.SILApplication = get_object_or_404(
            models.SILApplication.objects.select_for_update(), pk=application_pk
        )
        goods: Goods = get_object_or_404(goods_class, pk=goods_pk)

        task = application.get_task(ImportApplication.IN_PROGRESS, "prepare")

        if not request.user.has_perm("web.is_contact_of_importer", application.importer):
            raise PermissionDenied

        if request.POST:
            form = form_class(request.POST, instance=goods)
            if form.is_valid():
                goods = form.save(commit=False)
                goods.import_application = application
        else:
            form = form_class(instance=goods)

        context = {
            "process_template": "web/domains/case/import/partials/process.html",
            "process": application,
            "task": task,
            "form": form,
            "page_title": "Firearms and Ammunition (Specific Import Licence) - Edit Goods",
        }

        return render(request, template, context)


@login_required
@permission_required("web.importer_access", raise_exception=True)
@require_POST
def delete_section1(request: HttpRequest, *, application_pk: int, goods_pk: int) -> HttpResponse:
    goods_class = models.SILGoodsSection1
    return _delete_goods(request, application_pk, goods_pk, goods_class)


@login_required
@permission_required("web.importer_access", raise_exception=True)
@require_POST
def delete_section2(request: HttpRequest, *, application_pk: int, goods_pk: int) -> HttpResponse:
    goods_class = models.SILGoodsSection2
    return _delete_goods(request, application_pk, goods_pk, goods_class)


@login_required
@permission_required("web.importer_access", raise_exception=True)
@require_POST
def delete_section5(request: HttpRequest, *, application_pk: int, goods_pk: int) -> HttpResponse:
    goods_class = models.SILGoodsSection5
    return _delete_goods(request, application_pk, goods_pk, goods_class)


@login_required
@permission_required("web.importer_access", raise_exception=True)
@require_POST
def delete_section582_other(
    request: HttpRequest, *, application_pk: int, goods_pk: int
) -> HttpResponse:
    goods_class = models.SILGoodsSection582Other
    return _delete_goods(request, application_pk, goods_pk, goods_class)


@login_required
@permission_required("web.importer_access", raise_exception=True)
@require_POST
def delete_section582_obsolete(
    request: HttpRequest, *, application_pk: int, goods_pk: int
) -> HttpResponse:
    goods_class = models.SILGoodsSection582Obsolete
    return _delete_goods(request, application_pk, goods_pk, goods_class)


def _delete_goods(
    request: HttpRequest,
    application_pk: int,
    goods_pk: int,
    goods_class: GoodsT,
) -> HttpResponse:
    with transaction.atomic():
        application: models.SILApplication = get_object_or_404(
            models.SILApplication.objects.select_for_update(), pk=application_pk
        )
        goods: Goods = get_object_or_404(goods_class, pk=goods_pk)

        application.get_task(ImportApplication.IN_PROGRESS, "prepare")

        if not request.user.has_perm("web.is_contact_of_importer", application.importer):
            raise PermissionDenied

        goods.is_active = False
        goods.save()

        return redirect(reverse("import:fa-sil:edit", kwargs={"pk": application_pk}))
