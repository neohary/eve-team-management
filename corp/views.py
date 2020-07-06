from django.shortcuts import render
from .models import EveCorporation,EveCharacter,InvStorage,sellState,corpMiniBlog
from order.models import Order
from sde.models import Invtypes
from django.views import generic
from django.contrib.auth.models import User,Group
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from notifications.signals import notify
from django.utils import timezone
from django.db import transaction
from django.db.models import Sum,Q
# Create your views here.

@login_required
def index(request): #军团首页视图
    if request.user.groups.filter(pk=5).exists():
        corpcount = EveCorporation.objects.all().count()
        corps = EveCorporation.objects.filter(refuseVerification=False)
        character = EveCharacter.objects.count()
        context = {
            'corps':corps,
            'corpcount':corpcount,
            'character':character,
        }
        return render(request,'corp_index.html',context=context)
    else:
        return redirect('corp-detail',pk=request.user.profile.pcharacter.corp_id)
    
class characterInfView(LoginRequiredMixin,generic.DetailView): #角色详情
    model = EveCharacter
    
class corpInfView(LoginRequiredMixin,generic.DetailView): #军团详情
    model = EveCorporation
    
    @transaction.atomic
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs['pk']
        if self.request.user.profile.pcharacter.corp.id != pk:
            raise PermissionDenied
        else:
            context['users'] = User.objects.filter(profile__pcharacter__corp_id=pk).count()
            context['members'] = EveCharacter.objects.filter(corp_id=pk).count()
            context['completedorders'] = Order.objects.filter(corp_id=pk).filter(status='f').count()
            nowtime = timezone.now()
            context['monthlysales'] = Order.objects.filter(corp_id=pk).filter(finishdate__month=nowtime.month).aggregate(Sum('totalprice'))
            try:
                with urllib.request.urlopen("https://esi.evepc.163.com/latest/status/?datasource=serenity") as url:
                    data = json.loads(url.read().decode())
            except:
                context['players'] = "ESI错误"
            else:
                context['players'] = data['players']
            
            context['miniblogs'] = corpMiniBlog.objects.filter(corp=self.request.user.profile.pcharacter.corp_id)[:5]
            return context
        
class invStorageView(PermissionRequiredMixin,LoginRequiredMixin,generic.ListView): #军团库存视图
    permission_required = 'corp.can_update_invstorage'
    model = InvStorage
    template_name = "corp/storage_list.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs['pk']
        if self.request.user.profile.pcharacter.corp.id != pk:
            raise PermissionDenied
        else:
            pk = self.kwargs['pk']
            context['storage'] = InvStorage.objects.filter(corp_id=pk)
            return context
        
        
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from datetime import datetime
from .forms import pasteInvUpdateForm
import logging
import pandas as pd
from django.http import JsonResponse
import string


@permission_required('corp.can_update_invstorage')
@transaction.atomic
@login_required
def paste_storage_update(request,pk): #库存更新表单
    stor = InvStorage.objects.filter(corp_id=pk)
    corp = get_object_or_404(EveCorporation,pk=pk)
        
    if request.method == 'POST':
        form = pasteInvUpdateForm(request.POST)
        if form.is_valid():
            data = form.clean_raw_data()
            data_lines = data.splitlines()
            name = []
            value = []
            count = 0
            for data in data_lines:
                sdata = data.rsplit(' ',maxsplit = 1)[0] # I don't know why it works, but it works
                name.append(sdata.split('\t')[0])
                try:
                    num = str(sdata.split('\t')[1])
                    print("rawnum:"+num)
                    num = ''.join(ch for ch in num if ch not in string.punctuation)
                    print("pnum:"+num)
                    value.append(int(num))
                except IndexError:
                    response = JsonResponse({'error':"WRONG FORMAT"})
                    response.status_code = 403
                    return response
                except ValueError:
                    value.append(1)
            datalist = tuple(zip(name,value))
            dfdata = pd.DataFrame(datalist)
            dfdata.rename(columns={0:'name',1:'stock'},inplace=True)
            sdata = dfdata.groupby('name',as_index=False).sum()
            final_datalist = sdata.to_dict('r')
            #print(final_datalist)
            for item in final_datalist:
                try:
                    tempitem = Invtypes.objects.get(typename=item['name'])
                except Invtypes.MultipleObjectsReturned:
                    messages.error(request,"物品 {} 返回结果不唯一，自动忽略".format(item['name']))
                    continue
                except Invtypes.DoesNotExist:
                    messages.error(request,"物品 {} 不存在，自动忽略".format(item['name']))
                    continue
                    #response = JsonResponse({'error':"ITEM DOES NOT EXIST"})
                    #response.status_code = 403
                    #return response
                #搜索库存表 如果不存在则创建记录 如果存在就更新记录
                try:
                    record = InvStorage.objects.filter(corp_id=pk).filter(invtype=tempitem).get()
                except InvStorage.DoesNotExist:
                    temp = InvStorage(invtype=tempitem,corp_id=pk,stock=item['stock'])
                    temp.save()
                    count += 1
                else:
                    record.stock = item['stock']
                    record.update = timezone.now()
                    record.save()
                    count += 1
                    
            lg_group = User.objects.filter(profile__pcharacter__corp=request.user.profile.pcharacter.corp).filter(groups__id=1)
            
            if request.user.profile.nickname != None:
                rname = request.user.profile.nickname
            else:
                rname = request.user.get_username()
            
            messages.success(request,"已更新{}个物品到库存".format(count))
            notify.send(request.user,recipient=lg_group,verb="{}更新了{}的库存".format(rname,request.user.profile.pcharacter.corp),action_object=request.user)
            return HttpResponseRedirect(reverse('InvStorage-list',kwargs={'pk':pk}))
    else:
        if request.user.profile.pcharacter.corp.id != pk:
            raise PermissionDenied
        else:
            form = pasteInvUpdateForm()
        context = {
            'storage': stor,
            'corp': corp,
            'form': form,
        }
    
    return render(request,'corp/paste_storage_update.html',context=context)
    
    
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.core.exceptions import ValidationError
from .forms import ProfileForm
import urllib.request, json 
from urllib.parse import quote


class CharacterCreate(PermissionRequiredMixin,LoginRequiredMixin,CreateView): #创建角色
    permission_required = 'corp.user_can_create_characters'
    model = EveCharacter
    fields = ('name',)
    success_url = reverse_lazy('character-manage')
    def form_valid(self,form):
        obj = form.save(commit=False)
        obj.bounduser_id = self.request.user.id        
        try:
            with urllib.request.urlopen("https://esi.evepc.163.com/latest/search/?categories=character&datasource=serenity&language=zh&search={}&strict=true".format(quote(obj.name))) as url:
                data = json.loads(url.read().decode())
        except:
            messages.error(self.request,"ESI错误，请稍后重试")
            return redirect('character-manage')
        else:
            try:
                charid = data['character'][0]
            except:
                messages.error(self.request,"角色名错误")
                return redirect('character-manage')
        
        if EveCharacter.objects.filter(bounduser_id=self.request.user.id).count() >= 6:
            messages.error(self.request,"绑定角色已达上限")
            return redirect('character-manage')
        else:
            if self.request.user.profile.pcharacter != None:
                obj.ingame_id = charid
                obj.corp = self.request.user.profile.pcharacter.corp
                obj.save()
                self.object = obj
                messages.success(self.request,"成功创建并绑定角色 {}".format(obj.name))
                return HttpResponseRedirect(self.get_success_url())
            elif self.request.user.profile.pcharacter == None:
                obj.ingame_id = charid
                obj.save()
                self.object = obj
                messages.success(self.request,"成功创建并绑定角色 {}".format(obj.name))
                return HttpResponseRedirect(self.get_success_url())
    
    def form_invaild(self,form):
        messages.error(self.request,"角色名重复或其他错误，如果你的角色被其他人绑定了，请联系管理员")
        return redirect(self.request,'character_create')
        
class CharacterUpdate(PermissionRequiredMixin,LoginRequiredMixin,UpdateView): #修改角色
    permission_required = 'corp.user_can_create_characters'
    model = EveCharacter
    fields = ('name',)
    success_url = reverse_lazy('character-manage')
    
    def form_valid(self,form):
        obj = form.save(commit=False)
        obj.bounduser_id = self.request.user.id
        try:
            with urllib.request.urlopen("https://esi.evepc.163.com/latest/search/?categories=character&datasource=serenity&language=zh&search={}&strict=true".format(quote(obj.name))) as url:
                data = json.loads(url.read().decode())
        except:
            messages.error(self.request,"ESI错误，请稍后重试")
            return redirect('character-manage')
        else:
            try:
                charid = data['character'][0]
            except:
                messages.error(request,"角色名错误")
                return HttpResponseRedirect(self.get_success_url())
                
        if self.request.user.profile.pcharacter != None: #如果用户有主角色
            obj.ingame_id = charid
            obj.corp = self.request.user.profile.pcharacter.corp
            obj.save()
            self.object = obj
            return HttpResponseRedirect(self.get_success_url())
        elif self.request.user.profile.pcharacter == None: #如果用户没有主角色
            obj.ingame_id = charid
            obj.save()
            self.object = obj
            return HttpResponseRedirect(self.get_success_url())
    

class CharacterDelete(PermissionRequiredMixin,LoginRequiredMixin,DeleteView): #删除角色
    permission_required = 'corp.user_can_create_characters'
    model = EveCharacter
    success_url = reverse_lazy('character-manage')
    
    def delete(self,*args,**kwargs):
        self.object = self.get_object()
        if self.object.bounduser == self.request.user:
            if self.object == self.request.user.profile.pcharacter:
                raise PermissionDenied
            else:
                success_url = self.get_success_url()
                messages.success(self.request,"角色{}已经删除".format(self.object))
                self.object.delete()
                return HttpResponseRedirect(success_url)
        else:
            raise PermissionDenied
        
from django.db import transaction
from django.contrib import messages
from django.utils.translation import gettext as _
from django.shortcuts import redirect
from .models import Profile

class UserCharactersListView(LoginRequiredMixin,generic.ListView): #用户访问自己的角色列表
    model = EveCharacter
    template_name = 'corp/user_characters_manage.html'
    
    def get_queryset(self):
        return EveCharacter.objects.filter(bounduser_id=self.request.user.id).order_by('id')
        
@permission_required('corp.user_can_set_pcharacter')
@login_required
@transaction.atomic
def update_profile(request): #用户绑定主角色
    if request.user.profile.pcharacter == None: #如果用户没有主角色
        if request.method == 'POST': 
            profile_form = ProfileForm(data=request.POST,instance=request.user.profile)
            if profile_form.is_valid(): #如果表单有效
                profile_form.save()
                messages.success(request,_('主角色更新成功，现在你可以点击左侧边栏的“军团目录索引”选择一个军团并申请加入了。'))
                return redirect('character-manage')
            else:
                messages.error(request,_('Please correct the error below.'))
                return redirect('character-manage')
        else:
            profile_form = ProfileForm(user=request.user,instance=request.user.profile)
        return render(request,'corp/profile.html',{
            'profile_form':profile_form
        })
    else: #如果用户已经有主角色了 TODO:主角色一个月可以更换一次
        raise PermissionDenied
        
@login_required    
@transaction.atomic
def submit_verification(request,pk):
    if request.user.groups.filter(id=5).exists():
        if request.user.profile.pcharacter != None:
            if request.user.profile.pcharacter.corp == None:
                corp = EveCorporation.objects.get(pk=pk)
                if corp.refuseVerification == False:
                    characterlist = EveCharacter.objects.filter(bounduser=request.user)
                    for character in characterlist:
                        character.corp = corp
                        character.save()
        
                    corp_hr = User.objects.filter(profile__pcharacter__corp_id=pk).filter(groups__id=4)
            
                    if request.user.profile.nickname != None:
                        rname = request.user.profile.nickname
                    else:
                        rname = request.user.get_username()
                    notify.send(request.user,recipient=corp_hr,verb="{}提交了加入{}的申请".format(rname,corp),action_object=request.user)
                    notify.send(User.objects.get(pk=1),recipient=request.user,verb="你加入{}的申请已提交，请等待管理员审批".format(corp),action_object=request.user)
                    messages.success(request,"你加入{}的申请已提交，请等待管理员审批".format(corp))
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
                else:
                    messages.error(request,"{}当前不接受申请".format(corp))
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            else:
                messages.error(request,"你已经提交了加入{}的申请，不能再提交其他申请".format(request.user.profile.pcharacter.corp))
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            messages.error(request,"你还没有绑定主角色，请先点击左侧边栏中的“绑定角色管理”添加并指定一个主角色。")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
                
@permission_required('corp.corp_hr')
@login_required
@transaction.atomic
def verification_list(request,pk): #验证列表
    corp = EveCorporation.objects.get(pk=pk)
    if request.user.profile.pcharacter.corp == corp:
        v_userlist = User.objects.filter(profile__pcharacter__corp=corp).filter(groups__id=5)
        is_same_corp = []
        for user in v_userlist:
            try:
                with urllib.request.urlopen("https://esi.evepc.163.com/latest/characters/{}/?datasource=serenity".format(user.profile.pcharacter.ingame_id)) as url:
                    data = json.loads(url.read().decode())
            except:
                is_same_corp.append(None)
            else:
                
                is_player_same_corp = bool(user.profile.pcharacter.corp.ingame_id == data['corporation_id'])
                is_same_corp.append(is_player_same_corp)
                
        context = {
            'corp':corp,
            'userlist':zip(v_userlist,is_same_corp),
        }
        return render(request,'corp/verification_list.html',context=context)
    else:
        raise PermissionDenied
    
    
@login_required
@permission_required('corp.corp_hr')
@transaction.atomic
def verification_accept(request,pk): #验证通过
    user = User.objects.get(pk=pk)
    if request.user.profile.pcharacter.corp == user.profile.pcharacter.corp:
        if user.groups.filter(pk=5).exists():
            group = Group.objects.get(pk=3)
            user.groups.add(group)
            group = Group.objects.get(pk=5)
            user.groups.remove(group)
            
            if request.user.profile.nickname == None:
                rname = request.user.get_username()
            else:
                rname = request.user.profile.nickname
            
            hr_group = User.objects.filter(profile__pcharacter__corp=request.user.profile.pcharacter.corp).filter(groups__id=4)
            
            notify.send(request.user,recipient=user,verb="{}通过了你的申请，欢迎加入{}".format(rname,user.profile.pcharacter.corp),action_object=user)
            notify.send(request.user,recipient=hr_group,verb="{}同意了{}加入{}的申请".format(rname,user.get_username(),user.profile.pcharacter.corp),action_object=user)
            
            if user.profile.nickname == None:
                rname = user.get_username()
            else:
                rname = user.profile.nickname
            
            messages.success(request,"您批准了{}加入军团的申请".format(rname))
            return redirect('verification-list',pk=request.user.profile.pcharacter.corp.pk)
        else:
            messages.error(request,"该用户已离开验证队列")
            return redirect('verification-list',pk=request.user.profile.pcharacter.corp.pk)
    else:
        raise PermissionDenied
    
@login_required
@permission_required('corp.corp_hr')
@transaction.atomic
def verification_reject(request,pk): #验证拒绝
    user = User.objects.get(pk=pk)
    if request.user.profile.pcharacter.corp == user.profile.pcharacter.corp:
        if user.groups.filter(pk=5).exists():
            characterlist = EveCharacter.objects.filter(bounduser=user)
            for character in characterlist:
                character.corp = None
                character.save()
            
            if request.user.profile.nickname == None:
                rname = request.user.get_username()
            else:
                rname = request.user.profile.nickname
                
            hr_group = User.objects.filter(profile__pcharacter__corp=request.user.profile.pcharacter.corp).filter(groups__id=4)
            notify.send(request.user,recipient=user,verb="你加入{}的验证已被{}拒绝".format(user.profile.pcharacter.corp,rname),action_object=user)
            notify.send(request.user,recipient=hr_group,verb="{}拒绝了{}加入{}的申请".format(rname,user.get_username(),user.profile.pcharacter.corp),action_object=user)
            
            if user.profile.nickname == None:
                rname = user.get_username()
            else:
                rname = user.profile.nickname
            
            messages.success(request,"您拒绝了{}加入军团的申请".format(rname))
            return redirect('verification-list',pk=request.user.profile.pcharacter.corp.pk)
        else:
            messages.error(request,"该用户已离开验证队列")
            return redirect('verification-list',pk=request.user.profile.pcharacter.corp.pk)
    else:
        raise PermissionDenied
    
class sellStateListView(LoginRequiredMixin,PermissionRequiredMixin,generic.ListView):
    permission_required = 'corp.can_update_invstorage'
    model = sellState
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs['pk']
        if self.request.user.profile.pcharacter.corp.id != pk:
            raise PermissionDenied
        else:
            pk = self.kwargs['pk']
            context['sellstate'] = sellState.objects.filter(corp_id=pk)
            return context
    
def update_username(request):
    user = request.user
    
    try:
        user.profile.nickname = request.POST.get('nickname')
    except:
        messages.error(request,"用户名不可用，请重新输入")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        user.profile.save()
        messages.success(request,"用户名变更成功！")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
from .forms import corpMiniBlogForm,EveCorporationForm

@login_required
@permission_required('corp.corp_blogger')
@transaction.atomic
def corpMiniBlog_post(request,pk):
    corp = request.user.profile.pcharacter.corp
    if corp.id == pk:
        if request.method == "POST":
            form = corpMiniBlogForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                post.corp = corp
                post.poster = request.user
                corpPostList = corpMiniBlog.objects.filter(corp=corp).order_by('-posted')
                if corpMiniBlog.objects.filter(title=post.title).filter(body=post.body).exists():
                    messages.error(request,"完全相同的公告已存在，请勿重复提交。")
                    return redirect('corp-detail',pk=request.user.profile.pcharacter.corp_id)
                if corpPostList.count() > 10:
                    oldpost = corpPostList.reverse()[0]
                    oldpost.delete()
                post.save()
                messages.success(request,"公告已发布")
                return redirect('corp-detail',pk=request.user.profile.pcharacter.corp_id)
        else:
            form = corpMiniBlogForm()
            return render(request, 'corp/miniblog_post.html', {'form': form})
    else:
        raise PermissionDenied

@login_required 
@permission_required('corp.corp_blogger')
@transaction.atomic
def corpMiniBlog_delete(request,cpk,pk):
    try:
        post = corpMiniBlog.objects.get(pk=pk)
    except corpMiniBlog.DoesNotExist:
        messages.error(request,"公告已删除或不存在")
        return redirect('corp-detail',pk=request.user.profile.pcharacter.corp_id)
    else:
        if request.user.profile.pcharacter.corp == post.corp:
            post.delete()
            messages.success(request,"公告已删除")
            return redirect('corp-detail',pk=request.user.profile.pcharacter.corp_id)
        else:
            raise PermissionDenied
        
@login_required
@permission_required('corp.corp_info_edit')
@transaction.atomic
def corpInfUpdate(request,pk):
    corp = EveCorporation.objects.get(pk=pk)
    if request.user.profile.pcharacter.corp == corp:
        if request.method == 'POST':
            form = EveCorporationForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                print(post.dftdiscount)
                obj = EveCorporation.objects.get(pk=pk)
                obj.dftdiscount = post.dftdiscount
                obj.save()
                messages.success(request,"军团信息更新成功")
                return redirect('corp-detail',pk=corp.id)
            else:
                messages.error(request,"表单格式错误，请重试")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            form = EveCorporationForm(initial = {'dftdiscount':corp.dftdiscount})
            return render(request, 'corp/corp_inf_update.html', {'form': form})
    else:
        raise PermissionDenied
        
class corpMemberListView(LoginRequiredMixin,generic.ListView):
    model = EveCharacter
    template_name = 'corp/mem_list.html'
    
    @transaction.atomic
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs['pk']
        context['corp'] = EveCorporation.objects.filter(pk=pk).get()
        context['userlist'] = User.objects.filter(profile__pcharacter__corp_id=pk).order_by('id')
        context['evecharacter'] = EveCharacter.objects.filter(bounduser__profile__pcharacter__corp_id=pk).order_by('id')
        
        return context
            
class EveCorporationCreateView(LoginRequiredMixin,CreateView):
    model = EveCorporation
    fields = ('name','codename','alliance','dftdiscount')
    success_url = reverse_lazy('index')

@login_required
@transaction.atomic       
def cancel_verification(request):
    if request.user.profile.pcharacter.corp != None:
        characters = EveCharacter.objects.filter(bounduser=request.user)
        for character in characters:
            character.corp = None
            character.save()
            
        messages.error(request,"你撤回了申请")
        return redirect('index')
    else:
        messages.error(request,"你已经离开了军团")
        return redirect('index')
        
@login_required
@permission_required('corp.corp_hr')
@transaction.atomic
def hr_kickuser(request,username):
    try:
        user = User.objects.get(username=username)
    except:
        messages.error(request,"该用户不存在")
        return redirect('corp-mem-list',pk=request.user.profile.pcharacter.corp_id)
    else:
        if user.profile.nickname != None:
            uname = user.profile.nickname
        else:
            uname = user.get_username()
                
        if request.user.profile.pcharacter.corp == user.profile.pcharacter.corp:
            if user.groups.filter(Q(id=2) | Q(id=4) | Q(id=1) | Q(id=8) | Q(id=7)).exists():
                messages.error(request,"不能移除有重要职位的角色")
                return redirect('corp-mem-list',pk=request.user.profile.pcharacter.corp_id)
            else:
                characterlist = EveCharacter.objects.filter(bounduser=user)
                for character in characterlist:
                    character.corp = None
                    character.save()
                user.profile.dkp = 0
                user.groups.clear()
                user.profile.save()
                messages.success(request,"{}已被你移出军团".format(uname))
                initgroup = Group.objects.get(id=5)
                user.groups.add(initgroup)
                if request.user.profile.nickname != None:
                    rname = request.user.profile.nickname
                else:
                    rname = request.user.get_username()
                
                hr_group = User.objects.filter(profile__pcharacter__corp=request.user.profile.pcharacter.corp).filter(groups__id=4)
                
                notify.send(request.user,recipient=hr_group,verb="{}已被{}移出{}".format(uname,rname,request.user.profile.pcharacter.corp),action_object=request.user)
                notify.send(request.user,recipient=user,verb="你已被{}移出{}".format(rname,request.user.profile.pcharacter.corp),action_object=request.user)
                return redirect('corp-mem-list',pk=request.user.profile.pcharacter.corp_id)
        else:
            messages.error(request,"该用户不属于你的军团")
            return redirect('corp-mem-list',pk=request.user.profile.pcharacter.corp_id)
        

from .forms import UserGroupsForm     

class UserGroupsUpdateView(UpdateView):
    model = User
    template_name = 'corp/user_form.html'
    
    def get_initial(self):
        try:
            corp = self.object.profile.pcharacter.corp
        except:
            raise PermissionDenied
        else:
            if corp != self.request.user.profile.pcharacter.corp:
                raise PermissionDenied
            else:
                initial = super(UserGroupsUpdateView,self).get_initial()
                current_groups = self.object.groups.all()
                print(current_groups)
                initial['groups'] = current_groups
    
    def get_form_class(self):
        return UserGroupsForm
        
    def form_valid(self,form):
        self.object.groups.add(form.cleaned_data['groups'])
        return super(UserGroupsUpdateView,self).form_valid(form)
        
'''def hr_givejob(request,pk):
    try:
        user = User.objects.get(pk=pk)
    except:
        messages.error(request,"用户不存在")
        return redirect('corp-mem-list',pk=request.user.profile.pcharacter.corp_id)
    else:
        if request.user.groups.filter(pk=4).exists() and request.user.profile.pcharacter.corp == user.profile.pcharacter.corp:
            if request.method == 'POST':
            
            else:
                
            return 0'''
    
def quitcorp(request):
    try:
        corp = request.user.profile.pcharacter.corp
    except:
        messages.error(request,"退出军团时发生错误")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        if request.user.groups.filter(Q(id=2) | Q(id=4) | Q(id=1) | Q(id=8) | Q(id=7)).exists():
            messages.error(request,"不能移除有重要职位的角色")
            return redirect('corp-mem-list',pk=request.user.profile.pcharacter.corp_id)
        else:
            characterlist = EveCharacter.objects.filter(bounduser=request.user)
            for character in characterlist:
                character.corp = None
                character.save()
            request.user.profile.dkp = 0
            request.user.groups.clear()
            request.user.profile.save()
            initgroup = Group.objects.get(id=5)
            request.user.groups.add(initgroup)
            
            if request.user.profile.nickname != None:
                rname = request.user.profile.nickname
            else:
                rname = request.user.get_username()
            
            hr_group = User.objects.filter(profile__pcharacter__corp=request.user.profile.pcharacter.corp).filter(groups__id=4)
            
            notify.send(request.user,recipient=hr_group,verb="{}已退出{}".format(rname,corp),action_object=request.user)
            notify.send(request.user,recipient=request.user,verb="您已退出{}".format(corp),action_object=request.user)
            messages.success(request,"您已退出{}".format(corp))
    return redirect('character-manage')