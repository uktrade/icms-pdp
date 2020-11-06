import structlog as logging
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django.forms.widgets import Select, Textarea

from .approval.models import ApprovalRequest
from .models import AccessRequest

logger = logging.getLogger(__name__)


def is_valid(form, data, fields):
    """
        Check if fields in given list is entered by user
    """
    valid = True
    for field in fields:
        logger.debug(f"field {field}: {data[field]}")
        if not data[field]:
            valid = False
            form.add_error(field, "You must enter this item")

    logger.debug(f"Form valid? {valid}")
    return valid


def is_agent_request(request_type):
    # TODO: check if access request is for agent to make agent fields required
    return True


class ExporterAccessRequestForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        if is_agent_request():
            logger.debug("Validating agent")
            # Only validate agent_name and agent_address if this is an agent request
            if not is_valid(self, cleaned_data, ["agent_name", "agent_address"]):
                raise ValidationError("")
        return cleaned_data

    class Meta:
        model = AccessRequest

        fields = [
            "organisation_name",
            "organisation_address",
            "agent_name",
            "agent_address",
        ]

        widgets = {
            "organisation_address": Textarea({"rows": 5}),
            "agent_address": Textarea({"rows": 5}),
        }


class ImporterAccessRequestForm(ExporterAccessRequestForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        if not is_valid(self, cleaned_data, ["request_reason"]):
            raise ValidationError("")

    class Meta(ExporterAccessRequestForm.Meta):
        fields = [
            "organisation_name",
            "organisation_address",
            "request_reason",
            "agent_name",
            "agent_address",
        ]

        labels = {"request_reason": "What are you importing and where are you importing it from?"}

        widgets = ExporterAccessRequestForm.Meta.widgets
        widgets["request_reason"] = Textarea({"rows": 5})


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
