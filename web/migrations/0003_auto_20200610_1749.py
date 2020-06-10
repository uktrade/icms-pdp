# Generated by Django 2.2.10 on 2020-06-10 17:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0002_accessrequestprocess_approvalrequestprocess'),
    ]

    operations = [
        migrations.AlterField(
            model_name='baseteam',
            name='members',
            field=models.ManyToManyField(related_name='teams', to='web.User'),
        ),
        migrations.AlterField(
            model_name='role',
            name='team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='roles', to='web.BaseTeam'),
        ),
    ]