# Generated by Django 3.0.5 on 2020-05-29 09:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sde', '0002_auto_20200528_2102'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invtypes',
            name='marketgroupid',
            field=models.ForeignKey(blank=True, db_column='marketgroupID', null=True, on_delete=django.db.models.deletion.SET_NULL, to='sde.Marketgroups'),
        ),
    ]
