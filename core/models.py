from django.db import models

# Create your models here.
class generalMiniBlog(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField()
    posted = models.DateTimeField(db_index=True, auto_now_add=True)
    expire = models.DateTimeField(null=False,blank=False)
    
    def __str__(self):
        return self.title
        
class generalInfo(models.Model):
    siteTitle = models.CharField(max_length=100)
    subTitle = models.CharField(max_length=100)
    footInfo = models.CharField(max_length=100)
    version = models.CharField(max_length=100)
    inviteRegOnly = models.BooleanField(default=False,null=False,blank=False)
    underMaintaining = models.BooleanField(default=False,null=False,blank=False)
    
    def __str__(self):
        return self.siteTitle