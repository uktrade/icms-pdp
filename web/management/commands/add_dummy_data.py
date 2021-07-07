import datetime

from django.conf import settings
from django.contrib.auth.models import Permission
from django.core.management.base import BaseCommand, CommandError
from guardian.shortcuts import assign_perm

from web.domains.exporter.models import Exporter
from web.domains.importer.models import Importer
from web.domains.office.models import Office
from web.domains.user.models import User
from web.models import ImportApplicationType


class Command(BaseCommand):
    help = """Add dummy data. For development use only."""

    def add_arguments(self, parser):
        parser.add_argument(
            "--password",
            action="store",
            help="You must specify this to enable the command to run",
            required=True,
        )

    def handle(self, *args, **options):
        if settings.APP_ENV not in ("local", "dev"):
            raise CommandError("Can only add dummy data in 'dev' / 'local' environments!")

        self.activate_import_application_types()

        user = self.create_superuser(options["password"])
        agent = self.create_agent(options["password"])

        self.create_exporter(user, agent)
        self.create_importer(user, agent)

    def activate_import_application_types(self):
        # enable disabled application types so we can test/develop them
        ImportApplicationType.objects.filter(
            type__in=[
                ImportApplicationType.Types.OPT,
                ImportApplicationType.Types.TEXTILES,
                ImportApplicationType.Types.SPS,
            ]
        ).update(is_active=True)

    def create_superuser(self, password: str) -> User:
        try:
            user = User.objects.get(username="admin")

            self.stdout.write("Existing user: admin")
        except User.DoesNotExist:
            user = User.objects.create_superuser(
                username="admin",
                email="admin@blaa.com",
                password=password,
                first_name="admin",
                last_name="admin",
                date_of_birth=datetime.date(2000, 1, 1),
                security_question="admin",
                security_answer="admin",
            )

            self.stdout.write("Created following user: admin")

        # permissions
        for perm in [
            "importer_access",
            "exporter_access",
            "reference_data_access",
            "mailshot_access",
        ]:
            user.user_permissions.add(Permission.objects.get(codename=perm))

        user.save()

        return user

    def create_agent(self, password: str) -> User:
        try:
            agent = User.objects.get(username="agent")

            self.stdout.write("Existing user: agent")
        except User.DoesNotExist:
            agent = User.objects.create(
                username="agent",
                email="agent@blaa.com",
                first_name="agent",
                last_name="agent",
                date_of_birth=datetime.date(2000, 1, 1),
                security_question="agent",
                security_answer="agent",
                password_disposition=User.FULL,
            )
            agent.set_password(password)

            self.stdout.write("Created following user: agent")

        # permissions
        for perm in [
            "importer_access",
            "exporter_access",
        ]:
            agent.user_permissions.add(Permission.objects.get(codename=perm))

        agent.save()

        return agent

    def create_exporter(self, user: User, agent: User) -> None:
        exporter = Exporter.objects.create(
            is_active=True, name="Dummy exporter", registered_number="42"
        )
        assign_perm("web.is_contact_of_exporter", user, exporter)

        office = Office.objects.create(
            is_active=True, postcode="SW1A 1AA", address="Buckingham Palace, London"
        )
        exporter.offices.add(office)

        office = Office.objects.create(
            is_active=True, postcode="BT12 5QB", address="209 Roden St, Belfast"
        )
        exporter.offices.add(office)

        # agent for exporter
        agent_exporter = Exporter.objects.create(
            is_active=True,
            name="Agent for Dummy exporter",
            registered_number="4242",
            main_exporter=exporter,
        )
        assign_perm("web.is_agent_of_exporter", agent, exporter)
        assign_perm("web.is_contact_of_exporter", agent, agent_exporter)

        agent_office = Office.objects.create(
            is_active=True, postcode="TW6 2LA", address="Nettleton Rd, London"
        )
        agent_exporter.offices.add(agent_office)

        self.stdout.write(
            "Created dummy exporter and its agent with associated users: admin and agent"
        )

    def create_importer(self, user: User, agent: User) -> None:
        importer = Importer.objects.create(
            is_active=True,
            name="Dummy importer",
            registered_number="84",
            type=Importer.ORGANISATION,
        )
        assign_perm("web.is_contact_of_importer", user, importer)

        office = Office.objects.create(
            is_active=True, postcode="SW1A 2HP", address="3 Whitehall Pl, Westminster, London"
        )
        importer.offices.add(office)

        office = Office.objects.create(
            is_active=True, postcode="BT12 5QB", address="209 Roden St, Belfast"
        )
        importer.offices.add(office)

        # agent for importer
        agent_importer = Importer.objects.create(
            is_active=True,
            name="Agent for Dummy importer",
            registered_number="8484",
            type=Importer.ORGANISATION,
            main_importer=importer,
        )
        assign_perm("web.is_agent_of_importer", agent, importer)
        assign_perm("web.is_contact_of_importer", agent, agent_importer)

        agent_office = Office.objects.create(
            is_active=True, postcode="EN1 3SS", address="14 Mafeking Rd, Enfield"
        )
        agent_importer.offices.add(agent_office)

        self.stdout.write(
            "Created dummy importer and its agent with associated users: admin and agent"
        )
