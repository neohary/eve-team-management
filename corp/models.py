from django.db import models
from sde.models import Invtypes
from django.urls import reverse
from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save,pre_delete,post_delete
from django.dispatch import receiver
from copy import deepcopy

class EveAlliance(models.Model):
    name = models.CharField(max_length=20,help_text="输入联盟名称",unique=True)
    codename = models.CharField(max_length=20,help_text="联盟代号",unique=True)
    ingame_id = models.IntegerField(default=1,blank=False,null=False)
    
    def __str__(self):
        return self.name

class EveCorporation(models.Model):
    name = models.CharField(max_length=20,help_text="输入军团名称",unique=True)
    codename = models.CharField(max_length=20,help_text="军团代号",unique=True)
    alliance = models.ForeignKey('EveAlliance',on_delete=models.SET_NULL,null=True,blank=True)
    ceo = models.OneToOneField("EveCharacter",blank=True,null=True,on_delete=models.SET_NULL)
    ingame_id = models.IntegerField(default=1,blank=False,null=False)
    dftdiscount = models.IntegerField(default=100,blank=False,null=False)
    
    class Meta:
        permissions = (("corp_hr","军团人事相关的权限"),("corp_info_edit","更新军团设置的权限"))
    
    def get_absolute_url(self):
        return reverse('corp-detail', args=[str(self.id)])
        
    def __str__(self):
        return self.name
        
class EveCharacter(models.Model):
    name = models.CharField(max_length=20,help_text="输入游戏内的角色名，必须与游戏内的角色名称完全一致",unique=True)
    corp = models.ForeignKey("EveCorporation",on_delete=models.SET_NULL,null=True,blank=True)
    bounduser = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    ingame_id = models.IntegerField(default=1,blank=False,null=False)
    
    class Meta:
        permissions = (("user_can_create_characters","用户创建角色的权限"),)
    
    def get_absolute_url(self):
        return reverse('character-detail', args=[str(self.id)])
        
    def __str__(self):
        return self.name
        
        
class InvStorage(models.Model):
    invtype = models.ForeignKey(Invtypes,on_delete=models.CASCADE)
    corp = models.ForeignKey("EveCorporation",on_delete=models.CASCADE,null=False)
    stock = models.IntegerField(default=0,blank=False,null=False)
    sell = models.IntegerField(default=0,blank=False,null=False)
    updatetime = models.DateTimeField(auto_now_add=True, blank=True,null=True)
    sellclrdate = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        permissions = (("can_update_invstorage","更新库存数据的权限"),)
        
    def __str__(self):
        return '%s x %s (%s)' % (self.invtype.typename,self.stock,self.corp)
            

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    pcharacter = models.OneToOneField("EveCharacter",blank=True,null=True,on_delete=models.SET_NULL)
    nickname = models.CharField(max_length=12,unique=True,blank=True,null=True)
    dkp = models.IntegerField(default=0)
    donate = models.IntegerField(default=0)
    
    class Meta:
        permissions = (("user_can_set_pcharacter","用户设定主角色的权限"),)
    
    def __str__(self):
        return 'user:%s primarycharacter:%s' % (self.user,self.pcharacter)
    
@receiver(post_save,sender=User)
def create_user_profile(sender,instance,created,**kwargs):
    if created:
        Profile.objects.create(user=instance)
        
@receiver(post_save,sender=User)
def save_user_profile(sender,instance,**kwargs):
    instance.profile.save()
    
class sellState(models.Model):
    invtype = models.ForeignKey(Invtypes,on_delete=models.CASCADE)
    corp = models.ForeignKey("EveCorporation",on_delete=models.CASCADE,null=False)
    sell = models.IntegerField(default=0,blank=False,null=False)
    updatetime = models.DateTimeField(auto_now_add=True, blank=False)
    createdate = models.DateTimeField(auto_now_add=True,null=False, blank=False)
    
class corpMiniBlog(models.Model):
    title = models.CharField(max_length=20)
    body = models.TextField(max_length=500)
    posted = models.DateTimeField(db_index=True, auto_now_add=True)
    corp = models.ForeignKey('EveCorporation',on_delete=models.CASCADE,blank=False,null=False)
    poster = models.ForeignKey(User,on_delete=models.CASCADE,blank=False,null=False)
    
    class Meta:
        permissions = (("corp_blogger","编辑军团公告的权限"),)
        ordering = ["-posted"]
        
    def __str__(self):
        return '%s(%s)' % (self.title,self.corp)