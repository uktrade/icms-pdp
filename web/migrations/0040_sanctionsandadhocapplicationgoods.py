# Generated by Django 3.1.5 on 2021-03-02 15:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("web", "0039_woodquotaapplication"),
    ]

    operations = [
        migrations.CreateModel(
            name="SanctionsAndAdhocApplicationGoods",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("goods_description", models.TextField()),
                ("quantity_amount", models.CharField(max_length=1024)),
                ("value", models.CharField(max_length=1024)),
                (
                    "commodity_code",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT, to="web.commodity"
                    ),
                ),
                (
                    "import_application",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT, to="web.importapplication"
                    ),
                ),
            ],
        ),
    ]