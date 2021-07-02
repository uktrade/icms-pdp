from guardian.shortcuts import get_users_with_perms

from web.models import Exporter, User


def exporter_contacts(exporter: Exporter) -> User:
    """Active contacts associated with exporter/agent."""
    return get_users_with_perms(exporter, only_with_perms_in=["is_contact_of_exporter"]).filter(
        user_permissions__codename="exporter_access"
    )


def available_contacts(exporter: Exporter) -> User:
    contacts = exporter_contacts(exporter)
    available_contacts = User.objects.filter(
        is_active=True, user_permissions__codename="exporter_access"
    ).exclude(pk__in=contacts)

    return available_contacts
