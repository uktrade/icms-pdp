# Generated by Django 2.2.4 on 2019-08-30 12:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0056_auto_20190829_1235'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImportFurtherInformationRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('status', models.CharField(choices=[('DRAFT', 'Draft'), ('CLOSED', 'CLOSED'), ('DELETED', 'Deleted'), ('OPEN', 'Open'), ('RESPONDED', 'Responded')], default='DRAFT', max_length=20)),
                ('request_subject', models.CharField(max_length=100, null=True)),
                ('request_detail', models.CharField(max_length=4000, null=True)),
                ('email_cc_address_list', models.CharField(blank=True, max_length=4000, null=True)),
                ('requested_date', models.DateField(auto_now_add=True, null=True)),
                ('response_detail', models.CharField(max_length=4000, null=True)),
                ('response_date', models.DateField(blank=True, null=True)),
                ('closed_date', models.DateField(blank=True, null=True)),
                ('deleted_date', models.DateField(blank=True, null=True)),
                ('case', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='web.ImportCase')),
                ('closed_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='closed_import_information_requests', to='web.User')),
                ('deleted_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='deleted_import_information_requests', to='web.User')),
                ('requested_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='requested_further_import_information', to='web.User')),
                ('response_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='responded_import_information_requests', to='web.User')),
            ],
        ),
    ]