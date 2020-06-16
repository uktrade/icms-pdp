# Generated by Django 2.2.4 on 2019-09-05 16:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0062_exportcasevariation'),
    ]

    operations = [
        migrations.CreateModel(
            name='CaseNote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('status', models.CharField(choices=[('DRAFT', 'Draft'), ('DELETED', 'Deleted'), ('COMPLETED', 'Completed')], default='DRAFT', max_length=20)),
                ('note', models.TextField(blank=True, null=True)),
                ('create_datetime', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='created_import_case_notes', to='web.User')),
            ],
        ),
        migrations.CreateModel(
            name='FurtherInformationRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('status', models.CharField(choices=[('DRAFT', 'Draft'), ('CLOSED', 'CLOSED'), ('DELETED', 'Deleted'), ('OPEN', 'Open'), ('RESPONDED', 'Responded')], default='DRAFT', max_length=20)),
                ('request_subject', models.CharField(max_length=100, null=True)),
                ('request_detail', models.TextField(null=True)),
                ('email_cc_address_list', models.CharField(blank=True, max_length=4000, null=True)),
                ('requested_datetime', models.DateTimeField(auto_now_add=True, null=True)),
                ('response_detail', models.CharField(max_length=4000, null=True)),
                ('response_datetime', models.DateTimeField(blank=True, null=True)),
                ('closed_datetime', models.DateTimeField(blank=True, null=True)),
                ('deleted_datetime', models.DateTimeField(blank=True, null=True)),
                ('closed_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='closed_import_information_requests', to='web.User')),
                ('deleted_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='deleted_import_information_requests', to='web.User')),
                ('requested_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='requested_further_import_information', to='web.User')),
                ('response_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='responded_import_information_requests', to='web.User')),
            ],
        ),
        migrations.CreateModel(
            name='UpdateRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('status', models.CharField(max_length=30)),
                ('request_subject', models.CharField(max_length=100, null=True)),
                ('request_detail', models.TextField(null=True)),
                ('email_cc_address_list', models.CharField(blank=True, max_length=4000, null=True)),
                ('response_detail', models.TextField(null=True)),
                ('request_datetime', models.DateTimeField(blank=True, null=True)),
                ('response_datetime', models.DateTimeField(blank=True, null=True)),
                ('closed_datetime', models.DateTimeField(blank=True, null=True)),
                ('closed_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='closed_import_application_updates', to='web.User')),
                ('requested_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='requested_import_application_updates', to='web.User')),
                ('response_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='responded_import_application_updates', to='web.User')),
            ],
        ),
        migrations.CreateModel(
            name='VariationRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('status', models.CharField(choices=[('DRAFT', 'Draft'), ('OPEN', 'Open'), ('CANCELLED', 'Cancelled'), ('REJECTED', 'Rejected'), ('ACCEPTED', 'Accepted'), ('WITHDRAWN', 'Withdrawn'), ('DELETED', 'Deleted'), ('CLOSED', 'Closed')], max_length=30)),
                ('extension_flag', models.BooleanField(default=False)),
                ('requested_datetime', models.DateTimeField(auto_now_add=True, null=True)),
                ('what_varied', models.CharField(blank=True, max_length=4000, null=True)),
                ('why_varied', models.CharField(blank=True, max_length=4000, null=True)),
                ('when_varied', models.DateField(blank=True, null=True)),
                ('reject_reason', models.CharField(blank=True, max_length=4000, null=True)),
                ('closed_datetime', models.DateTimeField(blank=True, null=True)),
                ('closed_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='closed_variations', to='web.User')),
                ('requested_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='requested_variations', to='web.User')),
            ],
        ),
        migrations.RenameModel(
            old_name='CaseConstabularyEmail',
            new_name='ConstabularyEmail',
        ),
        migrations.RemoveField(
            model_name='importcasenote',
            name='case',
        ),
        migrations.RemoveField(
            model_name='importcasenote',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='importcasevariation',
            name='case',
        ),
        migrations.RemoveField(
            model_name='importcasevariation',
            name='requested_by',
        ),
        migrations.RemoveField(
            model_name='importfurtherinformationrequest',
            name='case',
        ),
        migrations.RemoveField(
            model_name='importfurtherinformationrequest',
            name='closed_by',
        ),
        migrations.RemoveField(
            model_name='importfurtherinformationrequest',
            name='deleted_by',
        ),
        migrations.RemoveField(
            model_name='importfurtherinformationrequest',
            name='requested_by',
        ),
        migrations.RemoveField(
            model_name='importfurtherinformationrequest',
            name='response_by',
        ),
        migrations.RemoveField(
            model_name='importupdaterequest',
            name='case',
        ),
        migrations.RemoveField(
            model_name='importupdaterequest',
            name='closed_by',
        ),
        migrations.RemoveField(
            model_name='importupdaterequest',
            name='requested_by',
        ),
        migrations.RemoveField(
            model_name='importupdaterequest',
            name='response_by',
        ),
        migrations.RemoveField(
            model_name='exportcase',
            name='application',
        ),
        migrations.RemoveField(
            model_name='importcase',
            name='application',
        ),
        migrations.AddField(
            model_name='exportapplication',
            name='case',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='application', to='web.ExportCase'),
        ),
        migrations.AddField(
            model_name='importapplication',
            name='case',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='application', to='web.ImportCase'),
        ),
        migrations.DeleteModel(
            name='ExportCaseVariation',
        ),
        migrations.DeleteModel(
            name='ImportCaseNote',
        ),
        migrations.DeleteModel(
            name='ImportCaseVariation',
        ),
        migrations.DeleteModel(
            name='ImportFurtherInformationRequest',
        ),
        migrations.DeleteModel(
            name='ImportUpdateRequest',
        ),
        migrations.AddField(
            model_name='accessrequest',
            name='further_information_requests',
            field=models.ManyToManyField(to='web.FurtherInformationRequest'),
        ),
        migrations.AddField(
            model_name='exportcase',
            name='case_notes',
            field=models.ManyToManyField(to='web.CaseNote'),
        ),
        migrations.AddField(
            model_name='exportcase',
            name='further_information_requests',
            field=models.ManyToManyField(to='web.FurtherInformationRequest'),
        ),
        migrations.AddField(
            model_name='exportcase',
            name='update_requests',
            field=models.ManyToManyField(to='web.UpdateRequest'),
        ),
        migrations.AddField(
            model_name='exportcase',
            name='variation_requests',
            field=models.ManyToManyField(to='web.VariationRequest'),
        ),
        migrations.AddField(
            model_name='importcase',
            name='case_notes',
            field=models.ManyToManyField(to='web.CaseNote'),
        ),
        migrations.AddField(
            model_name='importcase',
            name='further_information_requests',
            field=models.ManyToManyField(to='web.FurtherInformationRequest'),
        ),
        migrations.AddField(
            model_name='importcase',
            name='update_requests',
            field=models.ManyToManyField(to='web.UpdateRequest'),
        ),
        migrations.AddField(
            model_name='importcase',
            name='variation_requests',
            field=models.ManyToManyField(to='web.VariationRequest'),
        ),
    ]