import itertools

from django.conf import settings
from django.core.mail.message import EmailMultiAlternatives

from web.auth import utils as auth_utils
from web.domains.team.models import Role
from web.domains.user.models import AlternativeEmail, PersonalEmail, User


def send_email(subject, message, recipients, html_message=None, cc_list=None):
    """Sends emails to given recipients. cc_list: ";" separated email list"""
    if cc_list:
        cc_list = ",".join(cc_list.split(";"))

    email = EmailMultiAlternatives(
        subject=subject, body=message, from_email=settings.EMAIL_FROM, to=recipients
    )
    if html_message:
        email.attach_alternative(html_message, "text/html")

    email.send()


def get_user_emails_by_ids(user_ids):
    """Return a list emails for given users' ids"""
    personal = (
        PersonalEmail.objects.filter(user_id__in=user_ids)
        .filter(portal_notifications=True)
        .values_list("email", flat=True)
    )
    alternative = (
        AlternativeEmail.objects.filter(user_id__in=user_ids)
        .filter(portal_notifications=True)
        .values_list("email", flat=True)
    )
    queryset = personal.union(alternative)
    return list(queryset.all())


def get_role_member_notification_emails(role):
    """Return a list of emails for all active members of given role
        with portal notifications enabled"""
    user_ids = role.user_set.filter(account_status=User.ACTIVE).values_list("id", flat=True)
    return get_user_emails_by_ids(user_ids)


def get_notification_emails(user):
    """Returns user's personal and alternative email addresses
       with portal notifications enabled"""
    emails = []
    personal = user.personal_emails.filter(portal_notifications=True)
    alternative = user.alternative_emails.filter(portal_notifications=True)

    for email in itertools.chain(personal, alternative):
        if email.email and email.email not in emails:
            emails.append(email.email)

    return emails


def get_import_case_officers_emails():
    """Return a list of emails for import case officers"""
    return get_role_member_notification_emails(
        Role.objects.get(name="ILB Case Officers:Import Application Case Officer")
    )


def get_export_case_officers_emails():
    """Return a list of emails for export case officers"""
    return get_role_member_notification_emails(
        Role.objects.get(name="ILB Case Officers:Certificate Application Case Officer")
    )


def get_team_member_emails_with_permission(team, permission):
    """Return list of emails for team members with given permission"""
    users = auth_utils.get_team_members_with_permission(team, permission)
    user_ids = users.filter(account_status=User.ACTIVE).values_list("id", flat=True)
    return get_user_emails_by_ids(user_ids)
