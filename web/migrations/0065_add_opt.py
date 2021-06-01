# Generated by Django 3.1.8 on 2021-05-25 10:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("web", "0064_silgoodssections"),
    ]

    operations = [
        migrations.CreateModel(
            name="OutwardProcessingTradeApplication",
            fields=[
                (
                    "importapplication_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="web.importapplication",
                    ),
                ),
                (
                    "customs_office_name",
                    models.CharField(
                        max_length=100,
                        null=True,
                        verbose_name="Requested customs supervising office name",
                    ),
                ),
                (
                    "customs_office_address",
                    models.TextField(
                        max_length=4000,
                        null=True,
                        verbose_name="Requested customs supervising office address",
                    ),
                ),
                (
                    "rate_of_yield",
                    models.DecimalField(
                        decimal_places=2,
                        max_digits=9,
                        null=True,
                        verbose_name="Rate of yield (kg per garment)",
                    ),
                ),
                (
                    "rate_of_yield_calc_method",
                    models.TextField(
                        blank=True,
                        max_length=4000,
                        null=True,
                        verbose_name="Rate of yield calculation method",
                    ),
                ),
                (
                    "last_export_day",
                    models.DateField(
                        help_text="Requested last day of authorised exportation.", null=True
                    ),
                ),
                (
                    "reimport_period",
                    models.DecimalField(
                        decimal_places=2,
                        max_digits=9,
                        null=True,
                        verbose_name="Period for re-importation (months)",
                    ),
                ),
                (
                    "nature_process_ops",
                    models.TextField(
                        max_length=4000, null=True, verbose_name="Nature of processing operations"
                    ),
                ),
                (
                    "suggested_id",
                    models.TextField(
                        help_text="Enter the suggested means of identification of re-imported compensating products.",
                        max_length=4000,
                        null=True,
                        verbose_name="Suggested means of identification",
                    ),
                ),
                (
                    "supporting_documents",
                    models.ManyToManyField(
                        related_name="_outwardprocessingtradeapplication_supporting_documents_+",
                        to="web.File",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=("web.importapplication",),
        ),
        migrations.AlterField(
            model_name="importapplicationtype",
            name="type",
            field=models.CharField(
                choices=[
                    ("FA", "Firearms and Ammunition"),
                    ("SAN", "Derogation from Sanctions Import Ban"),
                    ("SAN_ADHOC_TEMP", "Sanctions and Adhoc"),
                    ("WD", "Wood (Quota)"),
                    ("OPT", "Outward Processing Trade"),
                ],
                max_length=70,
            ),
        ),
    ]