# Generated by Django 3.1.4 on 2020-12-31 09:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("web", "0009_actquantity_firearmsact"),
    ]

    operations = [
        migrations.CreateModel(
            name="EndorsementUsage",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                (
                    "application_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="+",
                        to="web.importapplicationtype",
                    ),
                ),
                ("linked_endorsements", models.ManyToManyField(to="web.Template")),
            ],
            options={
                "ordering": ("application_type__type",),
            },
        ),
    ]