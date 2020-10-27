# Generated by Django 3.1.2 on 2020-10-27 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("web", "0008_alter_verbose_name_importer_exporter"),
    ]

    operations = [
        migrations.AlterField(
            model_name="exporter",
            name="name",
            field=models.TextField(verbose_name="Organisation Name"),
        ),
        migrations.AlterField(
            model_name="importer",
            name="name",
            field=models.TextField(blank=True, null=True, verbose_name="Organisation Name"),
        ),
    ]
