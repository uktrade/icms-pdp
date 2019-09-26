# Generated by Django 2.2.4 on 2019-08-25 15:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0046_auto_20190822_1621'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommodityType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_code', models.CharField(max_length=20)),
                ('type', models.CharField(max_length=50)),
            ],
        ),
        migrations.AlterField(
            model_name='commodity',
            name='commodity_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='web.CommodityType'),
        ),
        migrations.AlterField(
            model_name='commoditygroup',
            name='commodity_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='web.CommodityType'),
        ),
    ]