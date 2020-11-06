import structlog as logging
from django.forms import Field, ModelForm, Select

from .approval.models import ApprovalRequest
from .models import AccessRequest, ExporterAccessRequest, ImporterAccessRequest

logger = logging.getLogger(__name__)


class ExporterAccessRequestForm(ModelForm):
    class Meta:
        model = ExporterAccessRequest

        fields = [
            "request_type",
            "organisation_name",
            "organisation_address",
            "organisation_registered_number",
            "agent_name",
            "agent_address",
        ]

    def clean(self):
        cleaned_data = super().clean()
        request_type = cleaned_data.get("request_type")
        if request_type == ExporterAccessRequest.AGENT_ACCESS:
            logger.debug("Validating agent")
            if not cleaned_data["agent_name"]:
                self.add_error("agent_name", Field.default_error_messages["required"])
            if not cleaned_data["agent_address"]:
                self.add_error("agent_address", Field.default_error_messages["required"])
        else:
            cleaned_data["agent_name"] = ""
            cleaned_data["agent_address"] = ""
        return cleaned_data


class ImporterAccessRequestForm(ModelForm):
    class Meta:
        model = ImporterAccessRequest

        fields = [
            "request_type",
            "organisation_name",
            "organisation_address",
            "organisation_registered_number",
            "eori_number",
            "eori_number_ni",
            "request_reason",
            "agent_name",
            "agent_address",
        ]

    def clean(self):
        cleaned_data = super().clean()
        request_type = cleaned_data.get("request_type")
        if request_type == ImporterAccessRequest.AGENT_ACCESS:
            logger.debug("Validating agent")
            if not cleaned_data["agent_name"]:
                self.add_error("agent_name", Field.default_error_messages["required"])
            if not cleaned_data["agent_address"]:
                self.add_error("agent_address", Field.default_error_messages["required"])
        else:
            cleaned_data["agent_name"] = ""
            cleaned_data["agent_address"] = ""
        return cleaned_data


class CloseAccessRequestForm(ModelForm):
    class Meta:
        model = AccessRequest

        fields = ["response", "response_reason"]


class ApprovalRequestForm(ModelForm):
    def __init__(self, team, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields[
            "requested_from"
        ].queryset = team.members.all()  # TODO: All members? Check if certain roles or not
        self.fields["requested_from"].empty_label = "All"

    class Meta:
        model = ApprovalRequest

        fields = ["requested_from"]

        labels = {"requested_from": "Contact"}

        widgets = {"requested_from": Select()}
