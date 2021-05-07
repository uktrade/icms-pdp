# Generated by Django 3.1.8 on 2021-05-07 08:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("web", "0060_alter_references"),
    ]

    operations = [
        migrations.CreateModel(
            name="DFLApplication",
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
                ("know_bought_from", models.BooleanField(null=True)),
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
                ],
                max_length=70,
                null=True,
            ),
        ),
    ]