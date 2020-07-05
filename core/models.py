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
    headInfo = models.TextField(max_length=500,null=True,blank=True)
    footInfo = models.TextField(max_length=1000)
    version = models.CharField(max_length=100)
    about = models.TextField(max_length=5000,null=True,blank=True)
    inviteRegOnly = models.BooleanField(default=False,null=False,blank=False)
    underMaintaining = models.BooleanField(default=False,null=False,blank=False)
    
    def __str__(self):
        return self.siteTitle
        
class donateInfo(models.Model):
    donater = models.CharField(max_length=100)
    amount = models.IntegerField(default=0)
    
    DONATE_TYPES = (
        ('r','RMB'),
        ('i','ISK'),
        ('o','其他'),
    )
    
    type = models.CharField(max_length=1, choices=DONATE_TYPES, blank=True, default='r',help_text='捐助类型')
    info = models.CharField(max_length=200,blank=True,null=True)
    donateDate = models.DateField(db_index=True, auto_now_add=True)
    
    class Meta:
        ordering = ['-amount']
    
    def __str__(self):
        return '%s (%s %s)' % (self.donater,self.amount,self.type)