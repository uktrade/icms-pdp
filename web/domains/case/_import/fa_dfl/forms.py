from typing import Any

from django import forms
from guardian.shortcuts import get_users_with_perms

from web.domains.case._import.forms import ChecklistBaseForm
from web.domains.file.utils import ICMSFileField
from web.models import Country

from . import models


class PrepareDFLForm(forms.ModelForm):
    deactivated_firearm = forms.BooleanField(disabled=True, label="Firearms Licence for")

    class Meta:
        model = models.DFLApplication
        fields = (
            "applicant_reference",
            "deactivated_firearm",
            "proof_checked",
            "origin_country",
            "consignment_country",
            "contact",
            "commodity_code",
            "constabulary",
            "know_bought_from",
        )

        help_texts = {
            "proof_checked": (
                "The firearm must have been proof marked as deactivated in line with current UK requirements"
            ),
            "origin_country": (
                "If the goods originate from more than one country,"
                " select the group (e.g. Any EU Country) that best describes this."
            ),
            "consignment_country": (
                "If the goods are consigned/dispatched from more than one country,"
                " select the group (e.g. Any EU Country) that best describes this."
            ),
            "commodity_code": (
                "You must pick the commodity code group that applies to the items that you wish to import."
                ' Please note that "ex Chapter 97" is only relevant to collectors pieces and items over 100 years old.'
                " Please contact HMRC classification advisory service, 01702 366077,"
                " if you are unsure of the correct code."
            ),
            "constabulary": "Select the constabulary in which you reside.",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["proof_checked"].required = True
        self.fields["know_bought_from"].required = True

        # The default label for unknown is "Unknown"
        self.fields["know_bought_from"].widget.choices = [
            ("unknown", "---------"),
            ("true", "Yes"),
            ("false", "No"),
        ]

        # TODO: ICMSLST-425 filter users here correctly (users with access to the importer)
        users = get_users_with_perms(
            self.instance.importer, only_with_perms_in=["is_contact_of_importer"]
        ).filter(is_active=True)
        self.fields["contact"].queryset = users

        countries = Country.objects.filter(
            country_groups__name="Firearms and Ammunition (Deactivated) Issuing Countries"
        )
        self.fields["origin_country"].queryset = countries
        self.fields["consignment_country"].queryset = countries


class AddDLFGoodsCertificateForm(forms.ModelForm):
    document = ICMSFileField(required=True)

    class Meta:
        model = models.DFLGoodsCertificate
        fields = ("goods_description", "deactivated_certificate_reference", "issuing_country")

        help_texts = {
            "goods_description": (
                "The firearm entered here must correspond with the firearm listed on the deactivation certificate."
                " You must list only one deactivated firearm per goods line."
            )
        }

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.fields["issuing_country"].queryset = Country.objects.filter(
            country_groups__name="Firearms and Ammunition (Deactivated) Issuing Countries"
        )


class EditDLFGoodsCertificateForm(forms.ModelForm):
    class Meta:
        model = models.DFLGoodsCertificate
        fields = ("goods_description", "deactivated_certificate_reference", "issuing_country")

        help_texts = {
            "goods_description": (
                "The firearm entered here must correspond with the firearm listed on the deactivation certificate."
                " You must list only one deactivated firearm per goods line."
            )
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        countries = Country.objects.filter(
            country_groups__name="Firearms and Ammunition (Deactivated) Issuing Countries"
        )

        self.fields["issuing_country"].queryset = countries


class EditDFLGoodsCertificateDescriptionForm(forms.ModelForm):
    class Meta:
        model = models.DFLGoodsCertificate
        fields = ("goods_description",)

        help_texts = {
            "goods_description": (
                "The firearm entered here must correspond with the firearm listed on the deactivation certificate."
                " You must list only one deactivated firearm per goods line."
            )
        }


class DFLChecklistForm(ChecklistBaseForm):
    class Meta:
        model = models.DFLChecklist

        fields = (
            "deactivation_certificate_attached",
            "deactivation_certificate_issued",
        ) + ChecklistBaseForm.Meta.fields


class DFLChecklistOptionalForm(DFLChecklistForm):
    """Used to enable partial saving of checklist."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for f in self.fields:
            self.fields[f].required = False
