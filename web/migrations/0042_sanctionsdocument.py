# Generated by Django 3.1.5 on 2021-03-12 12:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("web", "0041_alter_sanctions"),
    ]

    operations = [
        migrations.CreateModel(
            name="SanctionsDocument",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("file", models.FileField(upload_to="")),
                (
                    "import_application",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT, to="web.importapplication"
                    ),
                ),
                (
                    "uploaded_by",
                    models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to="web.user"),
                ),
            ],
        ),
    ]