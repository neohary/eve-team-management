from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect

from core.forms import SignUpForm,newLoginForm,donateInfoForm
from django.contrib.auth import login, authenticate

from django.views import View
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from order.models import Order
from django.db.models.signals import post_save
from django.contrib.auth.models import User, Group
from django.contrib import messages
from .models import generalInfo,donateInfo
from django.views import generic
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.db import transaction
# Create your views here.

@transaction.atomic
def signup(request):
    form_class = SignUpForm
    context = {}
    # if request is not post, initialize an empty form
    form = form_class(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username,password=raw_password)
            login(request,user)
            return redirect('index')
        else:
            context['signup_form'] = form
            #form = SignUpForm()
    else:
        form = SignUpForm()
        context['signup_form'] = form
    return render(request,'signup.html',context)
    
def add_user_to_base_group(sender,instance,created,**kwargs):
    try:
        if created:
            instance.groups.add(Group.objects.get(pk=5))
            print("ADD NEW USER TO BASE GROUP")
    except Group.DoesNotExist:
        pass

post_save.connect(add_user_to_base_group,sender=User)
    
    
class NoticeListView(LoginRequiredMixin,ListView):
    context_object_name = 'notices'
    template_name = 'core/notice/list.html'
    
    def get_queryset(self):
        return self.request.user.notifications.unread()
        
@transaction.atomic
def UpdateNotice(request):
    notice_id = request.GET.get('notice_id')
    
    if notice_id:
        order = Order.objects.get(id=request.GET.get('order_uid'))
        request.user.notifications.get(id=notice_id).mark_as_read()
        return redirect(order)
        
    else:
        request.user.notifications.mark_all_as_read()
        return redirect('notice-list')
    
class donateInfoListView(generic.ListView):
    model = donateInfo
    paginate_by = 40
    
def about(request):
    try:
        about = generalInfo.objects.get(pk=1).about
    except:
        about = "获取信息时出现错误"
        
    return render(request,'core/about.html',{'about':about})
    
from corp.models import EveCharacter

@login_required
@transaction.atomic
def addDonater(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            form = donateInfoForm(request.POST)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.save()
                
                if obj.type == 'r':
                    if EveCharacter.objects.filter(name=obj.donater).exists():
                        user = EveCharacter.objects.get(name=obj.donater).bounduser
                        user.profile.donate += obj.amount
                        user.save()
                    
                messages.success(request,"捐助记录添加成功")
                return redirect('donate-list')
            else:
                messages.error(request,"something wrong")
                form = donateInfoForm()
                return render(request,'core/add_donate.html',{'form':form})
        else:
            form = donateInfoForm()
            return render(request,'core/add_donate.html',{'form':form})
    else:
        raise PermissionDenied
    
    
    
    
    
    