from guardian.shortcuts import get_users_with_perms

from web.models import Importer, User


def importer_contacts(importer: Importer) -> User:
    """Active contacts associated with importer/agent."""
    return get_users_with_perms(importer, only_with_perms_in=["is_contact_of_importer"]).filter(
        user_permissions__codename="importer_access"
    )


def available_contacts(importer: Importer) -> User:
    contacts = importer_contacts(importer)
    available_contacts = User.objects.filter(
        is_active=True, user_permissions__codename="importer_access"
    ).exclude(pk__in=contacts)

    return available_contacts
