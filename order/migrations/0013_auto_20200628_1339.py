# Generated by Django 3.0.5 on 2020-06-28 05:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sde', '0004_auto_20200624_1759'),
        ('order', '0012_auto_20200628_1255'),
    ]

    operations = [
        migrations.AlterField(
            model_name='regularorderunit',
            name='item',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='sde.Invtypes'),
        ),
    ]
