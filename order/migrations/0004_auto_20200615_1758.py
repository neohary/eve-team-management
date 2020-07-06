# Generated by Django 3.0.5 on 2020-06-15 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0003_auto_20200615_0210'),
    ]

    operations = [
        migrations.AddField(
            model_name='regularorderunit',
            name='status',
            field=models.CharField(blank=True, choices=[('w', '等待处理'), ('s', '已发放'), ('p', '部分发放'), ('e', '缺货')], default='w', help_text='物品状态', max_length=1),
        ),
        migrations.AlterField(
            model_name='order',
            name='createdate',
            field=models.DateTimeField(auto_now_add=True, help_text='订单的创建日期'),
        ),
    ]
