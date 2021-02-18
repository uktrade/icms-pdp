from django import forms
from guardian.shortcuts import get_users_with_perms

from web.domains.country.models import Country
from web.domains.user.models import User


class SanctionsAndAdhocLicenseForm(forms.Form):

    contact = forms.ModelChoiceField(
        queryset=User.objects.none(),
        help_text="Select the main point of contact for the case. This will usually be the person who created the application.",
    )

    applicant_reference = forms.CharField(
        label="Applicant's Reference",
        help_text="Enter your own reference for this application.",
        required=False,
    )
    origin_country = forms.ModelChoiceField(
        label="Country Of Origin", empty_label=None, queryset=Country.objects.none()
    )
    consignment_country = forms.ModelChoiceField(
        label="Country Of Consignment", empty_label=None, queryset=Country.objects.none()
    )
    exporter_name = forms.CharField(
        label="Exporter Name",
        required=False,
    )
    exporter_address = forms.CharField(
        label="Exporter Address",
        required=False,
    )

    def __init__(self, *args, **kwargs):
        application = kwargs.get("application")
        del kwargs["application"]
        super().__init__(*args, **kwargs)
        users = get_users_with_perms(
            application.importer, only_with_perms_in=["is_contact_of_importer"]
        )
        self.fields["contact"].queryset = users.filter(is_active=True)
