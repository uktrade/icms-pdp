import structlog as logging
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import TemplateView
from viewflow.flow.views import FlowMixin, UpdateProcessView

from web.domains.exporter.views import ExporterListView
from web.domains.importer.views import ImporterListView
from web.flow.models import Task
from web.notify import notify
from web.views import ModelCreateView
from web.views.actions import Edit

from . import forms
from .actions import LinkExporter, LinkImporter
from .approval.models import ApprovalRequest
from .models import ExporterAccessRequest, ImporterAccessRequest

logger = logging.get_logger(__name__)


@login_required
def importer_access_request(request):
    with transaction.atomic():
        if request.POST:
            form = forms.ImporterAccessRequestForm(data=request.POST)
            if form.is_valid():
                application = form.save(commit=False)
                application.submitted_by = request.user
                application.last_update_by = request.user
                application.process_type = ImporterAccessRequest.PROCESS_TYPE
                application.save()

                notify.access_requested_importer(application.pk)
                Task.objects.create(process=application, task_type="request", owner=request.user)

                if request.user.is_importer() or request.user.is_exporter():
                    return redirect(reverse("workbasket"))

                # A new user who is not a member of any importer/exporter
                # is redirected to a different success page
                return redirect(reverse("access:requested"))
        else:
            form = forms.ImporterAccessRequestForm()

        context = {
            "form": form,
            "exporter_access_requests": ExporterAccessRequest.objects.filter(
                tasks__owner=request.user
            ),
            "importer_access_requests": ImporterAccessRequest.objects.filter(
                tasks__owner=request.user
            ),
        }

    return render(request, "web/domains/case/access/request-importer-access.html", context)


@login_required
def exporter_access_request(request):
    with transaction.atomic():
        form = forms.ExporterAccessRequestForm()
        if request.POST:
            form = forms.ExporterAccessRequestForm(data=request.POST)
            if form.is_valid():
                application = form.save(commit=False)
                application.submitted_by = request.user
                application.last_update_by = request.user
                application.process_type = ExporterAccessRequest.PROCESS_TYPE
                application.save()

                notify.access_requested_exporter(application.pk)
                Task.objects.create(process=application, task_type="request", owner=request.user)

                if request.user.is_importer() or request.user.is_exporter():
                    return redirect(reverse("workbasket"))

                # A new user who is not a member of any importer/exporter
                # is redirected to a different success page
                return redirect(reverse("access:requested"))

        context = {
            "form": form,
            "exporter_access_requests": ExporterAccessRequest.objects.filter(
                tasks__owner=request.user
            ),
            "importer_access_requests": ImporterAccessRequest.objects.filter(
                tasks__owner=request.user
            ),
        }

    return render(request, "web/domains/case/access/request-exporter-access.html", context)


class AccessRequestCreatedView(TemplateView):
    template_name = "web/domains/case/access/request-access-success.html"


class AccessRequestReviewView(ModelCreateView):
    template_name = "web/domains/case/access/review.html"
    permission_required = []
    model = ApprovalRequest

    def get_success_url(self):
        process = self.activation.process
        if process.approval_required:
            return reverse("workbasket")
        return super().get_success_url()

    def get_form(self):
        access_request = self.activation.process.access_request
        team = access_request.linked_importer or access_request.linked_exporter
        return forms.ApprovalRequestForm(team, data=self.request.POST or None)

    def _re_link(self):
        process = self.activation.process
        process.re_link = True
        process.save()
        self.activation.done()
        return redirect(self.get_success_url())

    def _close_request(self):
        process = self.activation.process
        process.approval_required = False
        process.save()
        self.activation.done()
        return redirect(self.get_success_url())

    def form_valid(self, form):
        """
            Save approval request
        """
        process = self.activation.process
        process.approval_required = True
        process.save()
        access_request = process.access_request
        approval_request = form.instance
        approval_request.access_request = access_request
        approval_request.requested_by = self.request.user
        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        if "_close_request" in request.POST:
            return self._close_request()
        elif "_re_link" in request.POST:
            return self._re_link()
        return super().post(request, *args, **kwargs)


class LinkImporterView(FlowMixin, ImporterListView):
    """
        Displays importer list view for searching and linking
        importers to access requests.
    """

    template_name = "web/domains/case/access/link-importer.html"

    def get_page_title(self):
        return f"{self.activation.process} - {self.activation.flow_task}"

    class Display(ImporterListView.Display):
        actions = [LinkImporter(), Edit()]

    def has_permission(self):
        # Viewflow protects this view,
        # no need to permissions of actual ImporterListView
        return True


class LinkExporterView(FlowMixin, ExporterListView):
    """
        Displays exporter list view for searching and linking
        exporter to access requests.
    """

    template_name = "web/domains/case/access/link-exporter.html"

    class Display(ExporterListView.Display):
        actions = [LinkExporter(), Edit()]

    def has_permission(self):
        # Viewflow protects this view,
        # no need to permissions of actual ExporterListView
        return True


class CloseAccessRequestView(UpdateProcessView):
    template_name = "web/domains/case/access/close.html"
    form_class = forms.CloseAccessRequestForm

    def _restart_approval(self):
        process = self.activation.process
        process.restart_approval = True
        process.save()
        self.activation.done()
        return redirect(self.get_success_url())

    def get_success_url(self):
        process = self.activation.process
        if process.restart_approval:
            return super().get_success_url()
        return reverse("workbasket")

    def get_approval_process(self):
        """
            Retrieves the approval process to be reviewed
        """
        process = self.activation.process
        flow_class = self.activation.flow_class
        flow_task = flow_class.approval
        approval_task = (
            flow_class.task_class._default_manager.filter(process=process, flow_task=flow_task)
            .order_by("-created")
            .first()
        )
        if approval_task:
            return approval_task.activate().subprocesses().first()

    def get_context_data(self, *args, **kwargs):
        """
            Adds latest approval process into context
        """
        context = super().get_context_data(*args, **kwargs)
        context["approval_process"] = self.get_approval_process()
        return context

    def post(self, request, *args, **kwargs):
        if "_restart_approval" in request.POST:
            return self._restart_approval()
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        process = self.activation.process
        open_firs = process.fir_processes.filter(finished__isnull=True)
        if open_firs.exists():
            with transaction.atomic():
                for fir_process in open_firs:
                    fir_process.cancel_process()
                    messages.success(self.request, "Cancelled FIRs")

        return super().form_valid(form)
