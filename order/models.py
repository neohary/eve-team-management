from django.db import models
from django.contrib.auth.models import User
from sde.models import Invtypes
from corp.models import EveCharacter,EveCorporation
from django.urls import reverse
import datetime
import uuid
# Create your models here.


class Order(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4,help_text="订单UID")
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    receiver = models.ForeignKey(EveCharacter,on_delete=models.CASCADE)
    corp = models.ForeignKey(EveCorporation,on_delete=models.CASCADE)
    totalprice = models.IntegerField(default=0,blank=False,null=False)
    discount = models.IntegerField(default=100,blank=False,null=False)
    itemcount = models.IntegerField(default=0,blank=False,null=False)
    
    ORDER_STATUS = (
        ('o','已提交'),
        ('f','已完成'),
        ('c','已取消'),
        ('p','进行中'),
    )
    
    status = models.CharField(max_length=1, choices=ORDER_STATUS, blank=True, default='o',help_text='订单状态')
    
    createdate = models.DateTimeField(auto_now_add=True,blank=True,help_text='订单的创建日期')
    finishdate = models.DateTimeField(blank=True,null=True,help_text='订单的完成日期')
    
    class Meta:
        ordering = ["-createdate"]
        permissions = (
        ("can_process_orders","查看成员订单、对其进行处理的权限"),
        ("user_can_create_orders","用户创建\取消订单的权限"),
        )
        
    def get_absolute_url(self):
        return reverse('order-detail', args=[str(self.uid)])
    
    def __str__(self):
        return '%s (%s-%s)' % (self.receiver,self.status,self.uid)
        
class regularOrderUnit(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4,help_text="单元UID")
    order = models.ForeignKey('Order',on_delete=models.CASCADE)
    item = models.ForeignKey(Invtypes,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0,blank=False,null=False,help_text="物品数量")
    price = models.IntegerField(default=0,blank=False,null=False,help_text="单价")
    
    ITEM_STATUS = (
        ('w','等待处理'),
        ('s','已发放'),
        ('p','等待发放'),
        ('e','无货'),
    )
    status = models.CharField(max_length=1, choices=ITEM_STATUS, blank=True, default='w',help_text='物品状态')
    
    def __str__(self):
        return '%s x %s (%s-%s)' % (self.item,self.quantity,self.status,self.uid)