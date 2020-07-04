# Generated by Django 3.0.5 on 2020-07-04 10:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('sde', '0001_initial'),
        ('corp', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('uid', models.UUIDField(default=uuid.uuid4, help_text='订单UID', primary_key=True, serialize=False)),
                ('totalprice', models.IntegerField(default=0)),
                ('discount', models.IntegerField(default=100)),
                ('itemcount', models.IntegerField(default=0)),
                ('status', models.CharField(blank=True, choices=[('o', '已提交'), ('f', '已完成'), ('c', '已取消'), ('p', '进行中')], default='o', help_text='订单状态', max_length=1)),
                ('createdate', models.DateTimeField(auto_now_add=True, help_text='订单的创建日期')),
                ('finishdate', models.DateTimeField(blank=True, help_text='订单的完成日期', null=True)),
                ('corp', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='corp.EveCorporation')),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='corp.EveCharacter')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-createdate'],
                'permissions': (('can_process_orders', '查看成员订单、对其进行处理的权限'), ('user_can_create_orders', '用户创建\\取消订单的权限')),
            },
        ),
        migrations.CreateModel(
            name='regularOrderUnit',
            fields=[
                ('uid', models.UUIDField(default=uuid.uuid4, help_text='单元UID', primary_key=True, serialize=False)),
                ('quantity', models.IntegerField(default=0, help_text='物品数量')),
                ('price', models.IntegerField(default=0, help_text='单价')),
                ('status', models.CharField(blank=True, choices=[('w', '等待处理'), ('s', '已发放'), ('p', '等待发放'), ('e', '无货')], default='w', help_text='物品状态', max_length=1)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sde.Invtypes')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order.Order')),
            ],
        ),
    ]
