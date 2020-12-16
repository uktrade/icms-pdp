# Generated by Django 3.1.4 on 2020-12-04 14:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("web", "0005_usage"),
    ]

    operations = [
        migrations.CreateModel(
            name="Section5Clause",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("clause", models.CharField(max_length=100)),
                ("description", models.TextField()),
                ("is_active", models.BooleanField(default=True)),
                ("created_datetime", models.DateTimeField(auto_now_add=True)),
                ("updated_datetime", models.DateTimeField(auto_now=True)),
                (
                    "created_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT, related_name="+", to="web.user"
                    ),
                ),
                (
                    "updated_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="+",
                        to="web.user",
                    ),
                ),
            ],
            options={
                "ordering": ("clause",),
            },
        ),
    ]
