# Generated by Django 3.1.8 on 2021-05-10 08:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("web", "0061_add_dflapplication"),
    ]

    operations = [
        migrations.CreateModel(
            name="SILUserSection5",
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
            ],
            bases=("web.file",),
        ),
        migrations.CreateModel(
            name="SILApplication",
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
                ("section1", models.BooleanField(null=True)),
                ("section2", models.BooleanField(null=True)),
                ("section5", models.BooleanField(null=True)),
                ("section58_obsolete", models.BooleanField(null=True)),
                ("section58_other", models.BooleanField(null=True)),
                ("other_description", models.CharField(blank=True, max_length=4000, null=True)),
                (
                    "military_police",
                    models.BooleanField(
                        null=True, verbose_name="Are any of your items for the military or police?"
                    ),
                ),
                (
                    "eu_single_market",
                    models.BooleanField(
                        null=True,
                        verbose_name="Were any of your items in the EU Single Market before 14 September 2018?",
                    ),
                ),
                (
                    "manufactured",
                    models.BooleanField(
                        null=True,
                        verbose_name="Were any of your items manufactured before 1 September 1939?",
                    ),
                ),
                ("commodity_code", models.CharField(max_length=40, null=True)),
                ("know_bought_from", models.BooleanField(null=True)),
                ("additional_comments", models.CharField(blank=True, max_length=4000, null=True)),
                (
                    "user_section5",
                    models.ManyToManyField(related_name="+", to="web.SILUserSection5"),
                ),
                (
                    "verified_section5",
                    models.ManyToManyField(related_name="+", to="web.Section5Authority"),
                ),
                (
                    "user_imported_certificates",
                    models.ManyToManyField(related_name="+", to="UserImportCertificate"),
                ),
            ],
            bases=("web.importapplication",),
        ),
        migrations.AlterField(
            model_name="importapplicationtype",
            name="sub_type",
            field=models.CharField(
                blank=True,
                choices=[
                    ("OIL", "Open Individual Import Licence"),
                    ("DEACTIVATED", "Deactivated Firearms Import Licence"),
                    ("SIL", "Specific Import Licence"),
                ],
                max_length=70,
                null=True,
            ),
        ),
    ]
