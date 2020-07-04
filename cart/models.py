from django.db import models
from django.contrib.auth.models import User
from sde.models import Invtypes
#from corp.models import EveCharacter
# Create your models here.

class Cart(models.Model):
    client = models.ForeignKey(User,on_delete=models.CASCADE)
    item = models.ForeignKey(Invtypes,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1,blank=False,null=False)
    price = models.IntegerField(default=0,blank=True,null=True)
    checkout = models.BooleanField(default=False)
    createdate = models.DateTimeField(auto_now_add=True,blank=True)
    
    class Meta:
        permissions = (("user_can_use_cart","用户使用购物车的权限"),)
    
    @property
    def get_total_price(self):
        return self.price * self.quantity
        
    def __str__(self):
        return '%s x %s' % (self.item,self.quantity)