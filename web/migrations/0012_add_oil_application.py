# Generated by Django 3.1.4 on 2021-01-11 16:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("web", "0011_add_cfs_schedule_data"),
    ]

    operations = [
        migrations.CreateModel(
            name="OpenIndividualLicenceApplication",
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
                    "verified_certificates",
                    models.ManyToManyField(
                        related_name="oil_application",
                        to="FirearmsAuthority",
                    ),
                ),
            ],
            bases=("web.importapplication",),
        ),
        migrations.RemoveField(
            model_name="importapplication",
            name="id",
        ),
        migrations.RemoveField(
            model_name="importapplication",
            name="is_active",
        ),
        migrations.RemoveField(
            model_name="importapplicationtype",
            name="sub_type_code",
        ),
        migrations.RemoveField(
            model_name="importapplicationtype",
            name="type_code",
        ),
        migrations.AddField(
            model_name="importapplication",
            name="process_ptr",
            field=models.OneToOneField(
                auto_created=True,
                default=None,
                on_delete=django.db.models.deletion.CASCADE,
                parent_link=True,
                primary_key=True,
                serialize=False,
                to="web.process",
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="importapplication",
            name="status",
            field=models.CharField(
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
                default="IN_PROGRESS",
                max_length=30,
            ),
        ),
        migrations.AlterField(
            model_name="importapplicationtype",
            name="sub_type",
            field=models.CharField(
                blank=True,
                choices=[("OIL", "Open Individual Import Licence")],
                max_length=70,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="importapplicationtype",
            name="type",
            field=models.CharField(choices=[("FA", "Firearms and Ammunition")], max_length=70),
        ),
    ]
