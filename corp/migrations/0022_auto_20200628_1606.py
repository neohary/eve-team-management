# Generated by Django 3.0.5 on 2020-06-28 08:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sde', '0004_auto_20200624_1759'),
        ('corp', '0021_auto_20200628_1553'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invstorage',
            name='invtype',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='sde.Invtypes'),
        ),
        migrations.AlterField(
            model_name='sellstate',
            name='invtype',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='sde.Invtypes'),
        ),
    ]
