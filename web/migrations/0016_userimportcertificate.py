# Generated by Django 3.1.4 on 2021-01-22 09:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("web", "0015_alter_oil_application"),
    ]

    operations = [
        migrations.CreateModel(
            name="UserImportCertificate",
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
                    "reference",
                    models.CharField(max_length=200, verbose_name="Certificate Reference"),
                ),
                (
                    "certificate_type",
                    models.CharField(
                        choices=[
                            ("firearms", "Firearms Certificate"),
                            ("registered", "Registered Firearms Dealer Certificate"),
                            ("shotgun", "Shotgun Certificate"),
                        ],
                        max_length=200,
                        verbose_name="Certificate Type",
                    ),
                ),
                ("date_issued", models.DateField(verbose_name="Date Issued")),
                ("expiry_date", models.DateField(verbose_name="Expiry Date")),
                ("updated_datetime", models.DateTimeField(auto_now=True)),
                (
                    "constabulary",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT, to="web.constabulary"
                    ),
                ),
            ],
            bases=("web.file",),
        ),
        migrations.AddField(
            model_name="openindividuallicenceapplication",
            name="user_imported_certificates",
            field=models.ManyToManyField(
                related_name="oil_application", to="UserImportCertificate"
            ),
        ),
    ]
