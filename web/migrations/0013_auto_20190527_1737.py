# Generated by Django 2.2.1 on 2019-05-27 17:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0012_alternativeemail_personalemail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='work_address',
            field=models.CharField(max_length=300, null=True),
        ),
    ]