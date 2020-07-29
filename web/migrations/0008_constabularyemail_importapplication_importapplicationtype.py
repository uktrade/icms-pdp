# Generated by Django 2.2.13 on 2020-07-29 16:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("web", "0007_furtherinformationrequestprocess"),
    ]

    operations = [
        migrations.CreateModel(
            name="ImportApplicationType",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("is_active", models.BooleanField()),
                ("type_code", models.CharField(max_length=30)),
                ("type", models.CharField(max_length=70)),
                ("sub_type_code", models.CharField(max_length=30)),
                ("sub_type", models.CharField(blank=True, max_length=70, null=True)),
                ("licence_type_code", models.CharField(max_length=20)),
                ("sigl_flag", models.BooleanField()),
                ("chief_flag", models.BooleanField()),
                ("chief_licence_prefix", models.CharField(blank=True, max_length=10, null=True)),
                ("paper_licence_flag", models.BooleanField()),
                ("electronic_licence_flag", models.BooleanField()),
                ("cover_letter_flag", models.BooleanField()),
                ("cover_letter_schedule_flag", models.BooleanField()),
                ("category_flag", models.BooleanField()),
                ("sigl_category_prefix", models.CharField(blank=True, max_length=100, null=True)),
                ("chief_category_prefix", models.CharField(blank=True, max_length=10, null=True)),
                ("default_licence_length_months", models.IntegerField(blank=True, null=True)),
                ("endorsements_flag", models.BooleanField()),
                ("default_commodity_desc", models.CharField(blank=True, max_length=200, null=True)),
                ("quantity_unlimited_flag", models.BooleanField()),
                ("unit_list_csv", models.CharField(blank=True, max_length=200, null=True)),
                ("exp_cert_upload_flag", models.BooleanField()),
                ("supporting_docs_upload_flag", models.BooleanField()),
                ("multiple_commodities_flag", models.BooleanField()),
                ("guidance_file_url", models.CharField(blank=True, max_length=4000, null=True)),
                (
                    "licence_category_description",
                    models.CharField(blank=True, max_length=1000, null=True),
                ),
                ("usage_auto_category_desc_flag", models.BooleanField()),
                ("case_checklist_flag", models.BooleanField()),
                ("importer_printable", models.BooleanField()),
                (
                    "commodity_type",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        to="web.CommodityType",
                    ),
                ),
                (
                    "consignment_country_group",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="import_application_types_to",
                        to="web.CountryGroup",
                    ),
                ),
                (
                    "declaration_template",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="declaration_application_types",
                        to="web.Template",
                    ),
                ),
                (
                    "default_commodity_group",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        to="web.CommodityGroup",
                    ),
                ),
                (
                    "endorsements",
                    models.ManyToManyField(
                        related_name="endorsement_application_types", to="web.Template"
                    ),
                ),
                (
                    "master_country_group",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="import_application_types",
                        to="web.CountryGroup",
                    ),
                ),
                (
                    "origin_country_group",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="import_application_types_from",
                        to="web.CountryGroup",
                    ),
                ),
            ],
            options={"ordering": ("type", "sub_type"),},
        ),
        migrations.CreateModel(
            name="ImportApplication",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("is_active", models.BooleanField(default=True)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("IN_PROGRESS", "In Progress"),
                            ("SUBMITTED", "Submitted"),
                            ("PROCESSING", "Processing"),
                            ("COMPLETED", "Completed"),
                            ("WITHDRAWN", "Withdrawn"),
                            ("STOPPED", "Stopped"),
                            ("REVOKED", "Revoked"),
                            ("VARIATION_REQUESTED", "Variation Requested"),
                            ("DELETED", "Deleted"),
                        ],
                        max_length=30,
                    ),
                ),
                ("reference", models.CharField(blank=True, max_length=50, null=True)),
                ("applicant_reference", models.CharField(blank=True, max_length=500, null=True)),
                ("submit_datetime", models.DateTimeField(blank=True, null=True)),
                ("create_datetime", models.DateTimeField(auto_now_add=True)),
                ("variation_no", models.IntegerField(default=0)),
                ("legacy_case_flag", models.BooleanField(default=False)),
                (
                    "chief_usage_status",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("C", "Cancelled"),
                            ("E", "Exhausted"),
                            ("D", "Expired"),
                            ("S", "S"),
                        ],
                        max_length=1,
                        null=True,
                    ),
                ),
                ("under_appeal_flag", models.BooleanField(default=False)),
                (
                    "decision",
                    models.CharField(
                        blank=True,
                        choices=[("REFUSE", "Refuse"), ("APPROVE", "Approve")],
                        max_length=10,
                        null=True,
                    ),
                ),
                (
                    "variation_decision",
                    models.CharField(
                        blank=True,
                        choices=[("REFUSE", "Refuse"), ("APPROVE", "Approve")],
                        max_length=10,
                        null=True,
                    ),
                ),
                ("refuse_reason", models.CharField(blank=True, max_length=4000, null=True)),
                (
                    "variation_refuse_reason",
                    models.CharField(blank=True, max_length=4000, null=True),
                ),
                ("issue_date", models.DateField(blank=True, null=True)),
                ("licence_start_date", models.DateField(blank=True, null=True)),
                ("licence_end_date", models.DateField(blank=True, null=True)),
                ("licence_extended_flag", models.BooleanField(default=False)),
                ("last_update_datetime", models.DateTimeField(auto_now=True)),
                (
                    "agent",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="agent_import_applications",
                        to="web.Importer",
                    ),
                ),
                (
                    "agent_office",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="agent_office_import_applications",
                        to="web.Office",
                    ),
                ),
                (
                    "application_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT, to="web.ImportApplicationType"
                    ),
                ),
                ("case_notes", models.ManyToManyField(to="web.CaseNote")),
                (
                    "consignment_country",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="import_applications_to",
                        to="web.Country",
                    ),
                ),
                (
                    "contact",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="contact_import_applications",
                        to="web.User",
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="created_import_applications",
                        to="web.User",
                    ),
                ),
                (
                    "further_information_requests",
                    models.ManyToManyField(to="web.FurtherInformationRequest"),
                ),
                (
                    "importer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="import_applications",
                        to="web.Importer",
                    ),
                ),
                (
                    "importer_office",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="office_import_applications",
                        to="web.Office",
                    ),
                ),
                (
                    "last_updated_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="updated_import_cases",
                        to="web.User",
                    ),
                ),
                (
                    "origin_country",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="import_applications_from",
                        to="web.Country",
                    ),
                ),
                (
                    "submitted_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="submitted_import_applications",
                        to="web.User",
                    ),
                ),
                ("update_requests", models.ManyToManyField(to="web.UpdateRequest")),
                ("variation_requests", models.ManyToManyField(to="web.VariationRequest")),
            ],
        ),
        migrations.CreateModel(
            name="ConstabularyEmail",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("is_active", models.BooleanField(default=True)),
                ("status", models.CharField(default="DRAFT", max_length=30)),
                ("email_cc_address_list", models.CharField(blank=True, max_length=4000, null=True)),
                ("email_subject", models.CharField(max_length=100, null=True)),
                ("email_body", models.TextField(max_length=4000, null=True)),
                ("email_response", models.TextField(blank=True, max_length=4000, null=True)),
                ("email_sent_datetime", models.DateTimeField(blank=True, null=True)),
                ("email_closed_datetime", models.DateTimeField(blank=True, null=True)),
                (
                    "application",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT, to="web.ImportApplication"
                    ),
                ),
            ],
        ),
    ]
