# Generated by Django 3.1.5 on 2021-02-05 11:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("web", "0020_withdrawimportapplication"),
    ]

    operations = [
        migrations.AddField(
            model_name="importapplication",
            name="case_owner",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="+",
                to="web.user",
            ),
        ),
    ]