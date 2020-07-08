from django import forms
from .models import Profile,EveCharacter,corpMiniBlog,EveCorporation

from django.contrib.auth.models import User, Group

class pasteInvUpdateForm(forms.Form): #粘贴式入库表单
    raw_data = forms.CharField(widget=forms.Textarea,help_text="在游戏内选择要更新的库存，Ctrl+C，然后Ctrl+V粘贴到此处",required=True)
    
    UPDATE_METHOD = (
        ('r','替换（REPLACE）'),
        ('a','添加（ADD）'),
    )
    
    update_method = forms.ChoiceField(widget=forms.RadioSelect,choices=UPDATE_METHOD,initial={'update_method':'r'},help_text="选择入库数据的更新方式：",required=True)
    
    def clean_raw_data(self):
        cleaned_raw_data = self.cleaned_data['raw_data']
        #d_lines_multi = cleaned_raw_data.splitlines()
        
        return cleaned_raw_data
        
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('pcharacter',)
    def __init__(self,user=None,**kwargs):
        super(ProfileForm,self).__init__(**kwargs)
        if user:
            self.fields['pcharacter'].queryset = EveCharacter.objects.filter(bounduser_id=user.id)
            
class corpMiniBlogForm(forms.ModelForm):
    class Meta:
        model = corpMiniBlog
        fields = ('title','body')
        widgets = {
            'title':forms.TextInput(attrs={'maxlength':14,'class':'form-control','placeholder':"标题"}),
            'body':forms.Textarea(attrs={'maxlength':500,'class':'form-control','placeholder':"正文"}),
        }
        
class EveCorporationForm(forms.ModelForm):
    class Meta:
        model = EveCorporation
        fields = ('dftdiscount',)
        widgets = {
            'dftdiscount':forms.NumberInput(attrs={'min':1,'max':100,'class':'form-control'})
        }
            
            
class UserGroupsForm(forms.ModelForm):
    groups = Group.objects.values_list('id','name').exclude(pk=5).exclude(pk=6).exclude(pk=2).exclude(pk=3)
    
    group = forms.MultipleChoiceField(choices = groups,
                                   widget=forms.CheckboxSelectMultiple,
                                   required=False)
    
    class Meta:
        model = User
        fields = ['group',]
        
        