# Generated by Django 3.1.5 on 2021-03-08 15:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("web", "0038_alter_importapplication_exportapplication"),
    ]

    operations = [
        migrations.CreateModel(
            name="WoodQuotaApplication",
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
                ("shipping_year", models.IntegerField(null=True)),
                ("exporter_name", models.CharField(max_length=100, null=True)),
                ("exporter_address", models.CharField(max_length=4000, null=True)),
                ("exporter_vat_nr", models.CharField(max_length=100, null=True)),
            ],
            bases=("web.importapplication",),
        ),
    ]
