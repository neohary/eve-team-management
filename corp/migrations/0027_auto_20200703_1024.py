# Generated by Django 3.0.5 on 2020-07-03 02:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('corp', '0026_auto_20200701_0839'),
    ]

    operations = [
        migrations.AlterField(
            model_name='corpminiblog',
            name='body',
            field=models.TextField(max_length=500),
        ),
        migrations.AlterField(
            model_name='corpminiblog',
            name='title',
            field=models.CharField(max_length=20),
        ),
    ]
