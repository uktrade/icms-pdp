# Generated by Django 3.1.12 on 2021-07-01 12:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("web", "0071_add_textiles"),
    ]

    operations = [
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
                    ("TEX", "Textiles (Quota)"),
                    ("SPS", "Prior Surveillance"),
                ],
                max_length=70,
            ),
        ),
        migrations.CreateModel(
            name="PriorSurveillanceContractFile",
            fields=[
                (
                    "file_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="web.file",
                    ),
                ),
                (
                    "file_type",
                    models.CharField(
                        choices=[
                            ("pro_forma_invoice", "Pro-forma Invoice"),
                            ("supply_contract", "Supply Contract"),
                        ],
                        max_length=32,
                    ),
                ),
            ],
            bases=("web.file",),
        ),
        migrations.CreateModel(
            name="PriorSurveillanceApplication",
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
                    "customs_cleared_to_uk",
                    models.BooleanField(
                        null=True,
                        help_text="If no, a paper licence will be issued for clearance in another EU Member State.",
                        verbose_name="Will the goods be customs cleared into the UK?",
                    ),
                ),
                (
                    "quantity",
                    models.PositiveIntegerField(
                        help_text="Please note that maximum allocations apply. Please check the guidance to ensure that you do not apply for more than is allowable.",
                        null=True,
                        verbose_name="Quantity",
                    ),
                ),
                (
                    "value_gbp",
                    models.PositiveIntegerField(
                        help_text="Round up to the nearest GBP. Do not enter decimal points, commas or any other punctuation in this box. The entered value will be automatically converted to EUR.",
                        null=True,
                        verbose_name="Value (GBP/£)",
                    ),
                ),
                (
                    "value_eur",
                    models.PositiveIntegerField(null=True, verbose_name="Value (EUR/€)"),
                ),
                (
                    "commodity",
                    models.ForeignKey(
                        help_text="It is the responsibility of the applicant to ensure that the commodity code in this box is correct. If you are unsure of the correct commodity code, consult the HM Revenue & Customs at classification.enquiries@hmrc.gsi.gov.uk or use the online trade tariff https://www.gov.uk/trade-tariff/sections.",
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="+",
                        to="web.commodity",
                        verbose_name="Commodity Code",
                    ),
                ),
                (
                    "contract_file",
                    models.OneToOneField(
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="+",
                        to="web.priorsurveillancecontractfile",
                    ),
                ),
                (
                    "supporting_documents",
                    models.ManyToManyField(
                        related_name="_priorsurveillanceapplication_supporting_documents_+",
                        to="web.File",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=("web.importapplication",),
        ),
    ]
