# Generated by Django 3.0.5 on 2020-07-03 02:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0016_auto_20200629_1920'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(blank=True, choices=[('o', '已提交'), ('f', '已完成'), ('c', '已取消'), ('p', '进行中')], default='o', help_text='订单状态', max_length=1),
        ),
        migrations.AlterField(
            model_name='regularorderunit',
            name='status',
            field=models.CharField(blank=True, choices=[('w', '等待处理'), ('s', '已发放'), ('p', '等待发放'), ('e', '无货')], default='w', help_text='物品状态', max_length=1),
        ),
    ]
