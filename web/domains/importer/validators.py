from django.core.exceptions import ValidationError


EORI_INDIVIDUAL_GB_PREFIX = "GBPR"
EORI_ORGANISATION_GB_PREFIX = "GB"


def eori_individual_gb(value):
    if value == EORI_INDIVIDUAL_GB_PREFIX:
        return
    raise ValidationError(f"'{value}' isn't a valid EORI number for an individual")


def eori_organisation_gb(value):
    if value.startswith(EORI_ORGANISATION_GB_PREFIX):
        return
    raise ValidationError(f"'value' doesn't start with {EORI_ORGANISATION_GB_PREFIX}")
