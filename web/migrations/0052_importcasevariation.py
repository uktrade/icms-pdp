# Generated by Django 2.2.4 on 2019-08-28 16:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0051_auto_20190828_1448'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImportCaseVariation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('status', models.CharField(choices=[('DRAFT', 'Draft'), ('OPEN', 'Open'), ('CANCELLED', 'Cancelled'), ('REJECTED', 'Rejected'), ('ACCEPTED', 'Accepted'), ('WITHDRAWN', 'Withdrawn')], max_length=30)),
                ('extension_flag', models.BooleanField(default=False)),
                ('requested_date', models.DateField(auto_now_add=True, null=True)),
                ('what_varied', models.CharField(blank=True, max_length=4000, null=True)),
                ('why_varied', models.CharField(blank=True, max_length=4000, null=True)),
                ('when_varied', models.DateField(blank=True, null=True)),
                ('reject_reason', models.CharField(blank=True, max_length=4000, null=True)),
                ('closed_date', models.DateField(blank=True, null=True)),
                ('case', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='web.ImportCase')),
                ('requested_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='web.User')),
            ],
        ),
    ]