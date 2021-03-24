# Generated by Django 3.1.5 on 2021-03-24 10:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("web", "0045_alter_derogations"),
    ]

    operations = [
        migrations.AddField(
            model_name="derogationsapplication",
            name="commodity_code",
            field=models.ForeignKey(
                null=True, on_delete=django.db.models.deletion.PROTECT, to="web.commodity"
            ),
        ),
        migrations.AddField(
            model_name="derogationsapplication",
            name="goods_description",
            field=models.CharField(max_length=4096, null=True),
        ),
        migrations.AddField(
            model_name="derogationsapplication",
            name="quantity_amount",
            field=models.DecimalField(decimal_places=2, max_digits=9, null=True),
        ),
        migrations.AddField(
            model_name="derogationsapplication",
            name="value",
            field=models.DecimalField(decimal_places=2, max_digits=9, null=True),
        ),
    ]
