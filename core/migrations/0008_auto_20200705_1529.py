# Generated by Django 3.0.5 on 2020-07-05 07:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_donateinfo'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='donateinfo',
            options={'ordering': ['-donateDate']},
        ),
        migrations.AlterField(
            model_name='donateinfo',
            name='info',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
