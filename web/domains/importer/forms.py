from dal import autocomplete
from django.forms.fields import ChoiceField, CharField
from django.forms.widgets import Textarea
from django_filters import CharFilter, ChoiceFilter
from web.forms import ModelEditForm, ModelSearchFilter
from web.forms.mixins import ReadonlyFormMixin, RequiredFieldsMixin
from django.db.models import Q

from web.domains.importer.models import Importer
from web.domains.importer.validators import eori_individual_gb, eori_organisation_gb


HELP_TEXT_EORI_NUMBER = "EORI number should include the GB or GBN prefix."
LABEL_EORI = "EORI Number"
LABEL_EORI_NI = "NI EORI Number"
LABEL_ORG_NAME = "Organisation Name"


class ImporterFilter(ModelSearchFilter):
    importer_entity_type = ChoiceFilter(
        field_name="type", choices=Importer.TYPES, label="Importer Entity Type"
    )

    status = ChoiceFilter(
        field_name="is_active",
        choices=((True, "Current"), (False, "Archived")),
        lookup_expr="exact",
        label="Status",
    )

    name = CharFilter(lookup_expr="icontains", label="Importer Name", method="filter_importer_name")

    agent_name = CharFilter(lookup_expr="icontains", label="Agent Name", method="filter_agent_name")

    # Filter base queryset to only get importers that are not agents.
    @property
    def qs(self):
        return super().qs.select_related("user").filter(main_importer__isnull=True)

    def filter_importer_name(self, queryset, name, value):
        if not value:
            return queryset

        #  Filter organisation name for organisations and title, first_name, last_name
        #  for individual importers
        return queryset.filter(
            Q(name__icontains=value)
            | Q(user__title__icontains=value)
            | Q(user__first_name__icontains=value)
            | Q(user__last_name__icontains=value)
        )

    def filter_agent_name(self, queryset, name, value):
        if not value:
            return queryset

        #  Filter agent name for organisations and title, first_name, last_name
        #  for individual importer agents
        return queryset.filter(
            Q(agents__name__icontains=value)
            | Q(agents__user__title__icontains=value)
            | Q(agents__user__first_name__icontains=value)
            | Q(agents__user__last_name__icontains=value)
        )

    class Meta:
        model = Importer
        fields = []


class ImporterIndividualForm(RequiredFieldsMixin, ModelEditForm):
    eori_number = CharField(
        validators=[eori_individual_gb], label=LABEL_EORI, help_text=HELP_TEXT_EORI_NUMBER
    )

    class Meta:
        model = Importer
        required = ["user", "eori_number"]
        fields = required + ["eori_number_ni", "region_origin", "comments"]
        widgets = {
            "user": autocomplete.ModelSelect2(
                url="user-autocomplete", attrs={"data-placeholder": "Search for a person"}
            ),
            "comments": Textarea({"rows": 5, "cols": 20}),
        }
        labels = {"eori_number_ni": LABEL_EORI_NI, "user": "Person"}

    def clean(self):
        self.instance.type = Importer.INDIVIDUAL
        return super().clean()


class ImporterOrganisationForm(RequiredFieldsMixin, ModelEditForm):
    eori_number = CharField(
        validators=[eori_organisation_gb], label=LABEL_EORI, help_text=HELP_TEXT_EORI_NUMBER
    )

    class Meta:
        model = Importer
        required = ["name", "eori_number"]
        fields = [
            "name",
            "registered_number",
            "eori_number",
            "eori_number_ni",
            "region_origin",
            "comments",
        ]
        widgets = {"comments": Textarea({"rows": 5, "cols": 20})}
        labels = {
            "eori_number": LABEL_EORI,
            "eori_number_ni": LABEL_EORI_NI,
            "name": LABEL_ORG_NAME,
        }
        help_texts = {"eori_number": HELP_TEXT_EORI_NUMBER}

    def clean(self):
        self.instance.type = Importer.ORGANISATION
        return super().clean()


class ImporterOrganisationEditForm(ModelEditForm):
    type = ChoiceField(choices=Importer.TYPES)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].required = True

    class Meta:
        model = Importer
        fields = ["type", "name", "region_origin", "comments"]
        labels = {"type": "Entity Type"}


class ImporterOrganisationDisplayForm(ReadonlyFormMixin, ImporterOrganisationEditForm):
    pass


class ImporterIndividualEditForm(ModelEditForm):
    type = ChoiceField(choices=Importer.TYPES)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["user"].required = True

    class Meta:
        model = Importer
        fields = ["type", "user", "comments"]


class ImporterIndividualDisplayForm(ReadonlyFormMixin, ModelEditForm):
    type = ChoiceField(choices=Importer.TYPES)

    # ImporterIndividualDetailView fills these out
    user_title = CharField(label="Title")
    user_first_name = CharField(label="Forename")
    user_last_name = CharField(label="Surname")
    user_email = CharField(label="Email")
    user_tel_no = CharField(label="Telephone No")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["user"].required = True

    class Meta:
        model = Importer
        fields = ["type", "user", "comments"]
