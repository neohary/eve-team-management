# Generated by Django 3.0.5 on 2020-06-25 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('corp', '0007_auto_20200624_0302'),
    ]

    operations = [
        migrations.AddField(
            model_name='evecorporation',
            name='dftdiscount',
            field=models.IntegerField(default=100),
        ),
    ]
