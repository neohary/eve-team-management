# Generated by Django 3.0.5 on 2020-07-05 03:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20200705_1127'),
    ]

    operations = [
        migrations.AlterField(
            model_name='generalinfo',
            name='footInfo',
            field=models.TextField(max_length=100),
        ),
        migrations.AlterField(
            model_name='generalinfo',
            name='headInfo',
            field=models.TextField(blank=True, max_length=100, null=True),
        ),
    ]
