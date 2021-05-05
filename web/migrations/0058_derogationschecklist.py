# Generated by Django 3.1.8 on 2021-04-29 10:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("web", "0057_add_constabulary_data"),
    ]

    operations = [
        migrations.CreateModel(
            name="DerogationsChecklist",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                (
                    "supporting_document_received",
                    models.CharField(
                        blank=True,
                        choices=[("yes", "Yes"), ("no", "No"), ("n/a", "N/A")],
                        max_length=10,
                        null=True,
                        verbose_name="Supporting documentation received?",
                    ),
                ),
                (
                    "case_update",
                    models.CharField(
                        blank=True,
                        choices=[("yes", "Yes"), ("no", "No"), ("n/a", "N/A")],
                        max_length=10,
                        null=True,
                        verbose_name="Case update required from applicant?",
                    ),
                ),
                (
                    "fir_required",
                    models.CharField(
                        blank=True,
                        choices=[("yes", "Yes"), ("no", "No"), ("n/a", "N/A")],
                        max_length=10,
                        null=True,
                        verbose_name="Further information request required?",
                    ),
                ),
                (
                    "response_preparation",
                    models.BooleanField(
                        default=False,
                        verbose_name="Response Preparation - approve/refuse the request, edit details if necessary",
                    ),
                ),
                (
                    "validity_period_correct",
                    models.CharField(
                        blank=True,
                        choices=[("yes", "Yes"), ("no", "No"), ("n/a", "N/A")],
                        max_length=10,
                        null=True,
                        verbose_name="Validity period correct?",
                    ),
                ),
                (
                    "endorsements_listed",
                    models.CharField(
                        blank=True,
                        choices=[("yes", "Yes"), ("no", "No"), ("n/a", "N/A")],
                        max_length=10,
                        null=True,
                        verbose_name="Correct endorsements listed? Add/edit/remove as required (changes are automatically saved)",
                    ),
                ),
                (
                    "authorisation",
                    models.BooleanField(
                        default=False,
                        verbose_name="Authorisation - start authorisation (close case processing) to authorise the licence. Errors logged must be resolved.",
                    ),
                ),
                (
                    "import_application",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="checklists",
                        to="web.derogationsapplication",
                    ),
                ),
            ],
        ),
    ]
