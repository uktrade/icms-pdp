import logging
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy

from web.views import ModelCreateView

from .forms import NewImportApplicationForm
from .models import ImportApplication, ImportApplicationType

from web.domains.importer.models import Importer
from web.domains.office.models import Office

logger = logging.getLogger(__name__)


def get_importers(user):
    main_importers = Q(members=user, main_importer__isnull=True)
    agent_importers = Q(pk__in=Importer.get_agent_importer_ids(user))

    importers = Importer.objects.filter(is_active=True)
    return importers.filter(main_importers | agent_importers)


def get_offices():
    return Office.objects.all()


def import_application_create_firearms_sil(request):
    type_code = "FA"
    type_sub_code = "SIL"
    logger.debug(f"import_application_create_firearms_specific {request.user} {type_code} {type_sub_code}")
    application_type = get_object_or_404(ImportApplicationType, type_code=type_code, sub_type_code=type_sub_code,
                                         is_active=True)

    importers = get_importers(request.user)
    logger.debug("There are %s importers" % importers.count())

    return render(request, "web/application/import/create_firearms_sil.html", {
        "application_type": application_type,
        "importers": importers,
        "offices": get_offices()
    })


def import_application_start(request):
    application_types = ImportApplicationType.objects.filter(is_active=True).order_by('type')

    return render(request, "web/application/import/start.html", {
        "application_types": application_types
    })


class ImportApplicationCreateView(ModelCreateView):
    template_name = 'web/application/import/create.html'
    model = ImportApplication

    # TODO: Change to application form when created

    success_url = reverse_lazy('product-legislation-list')
    cancel_url = success_url
    form_class = NewImportApplicationForm
    page_title = 'Create Import Application'

    def get_form(self):
        if hasattr(self, 'form'):
            return self.form

        if self.request.POST:
            self.form = NewImportApplicationForm(self.request,
                                                 data=self.request.POST)
        else:
            self.form = NewImportApplicationForm(self.request)

        return self.form

    def post(self, request, *args, **kwargs):
        if request.POST:
            if request.POST.get('change', None):
                return super().get(request, *args, **kwargs)

        form = self.get_form()
        form.instance.created_by = request.user

        return super().post(request, *args, **kwargs)

    def has_permission(self):
        return True
