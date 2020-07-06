from django.shortcuts import render
from .models import Order,regularOrderUnit
from sde.models import Invtypes
from corp.models import EveCharacter,InvStorage,sellState
from cart.models import Cart
from django.views import generic
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import requests
from django.shortcuts import redirect
from django.utils import timezone
from django.contrib import messages
from notifications.signals import notify
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db import transaction
from django.http import HttpResponseRedirect

# Create your views here.
@permission_required('order.user_can_create_orders')
@transaction.atomic
@login_required
def create_order(request): #创建订单
    if request.method == 'POST':
        cartlist = request.POST.getlist('cart') #获取提交的物品列表
        if cartlist:
            character = EveCharacter.objects.get(name=request.POST.get('character')) #获取收货角色
            order = Order(receiver=character,user=request.user,corp=character.corp,itemcount=len(cartlist)) #创建订单
            order.save()
            totalprice = 0
            for cart in cartlist:
                try:
                    r_cart = Cart.objects.filter(pk=cart).filter(client=request.user).get()
                except Cart.DoesNotExist:
                    order.delete()
                    messages.error(request,"订单已提交 请勿重复提交")
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
                    
                temp = regularOrderUnit(order=order,item=r_cart.item,quantity=r_cart.quantity,price=r_cart.price)
                temp.save()
                r_cart.delete()
                totalprice += temp.price * temp.quantity
            order.totalprice = totalprice
            try:
                order.save()
            except OverflowError:
                messages.error(request,"订单数值过大，请拆分提交")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
                
                    
            messages.success(request,"订单创建成功！")
            notify.send(User.objects.get(id=1),recipient=request.user,verb="你的订单{}已创建".format(order.uid),action_object=order)
        else:
            messages.error(request,"订单创建失败 请勾选要下单的物品")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        messages.error(request,"不能是GET请求")
        
    return render(request,'order/submit_order.html')

class orderListView(LoginRequiredMixin,generic.ListView):
    model = Order
    template_name = 'order/order_list.html'
        
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).exclude(status='c')
        
class orderDetailView(LoginRequiredMixin,generic.DetailView):
    model = Order
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs['pk']
        order = Order.objects.get(pk=pk)
        context['itemlist'] = regularOrderUnit.objects.filter(order=order)
        return context
        
@permission_required('order.user_can_create_orders')
@login_required
def cancel_order(request,pk): #用户取消订单
    order = Order.objects.get(pk=pk)
    if order.user == request.user:
        if order.status == 'o':
            regularOrderUnit.objects.filter(order=order).delete()
            order.status = 'c'
            order.save()
            messages.success(request,"订单{}已取消".format(order.uid))
        else:
            messages.error(request,"用户只能取消未完成的订单")
    else:
        messages.error(request,"你没有权限那样做")
    
    return redirect('my-orders')
    
    
class orderListViewCorp(LoginRequiredMixin,PermissionRequiredMixin,generic.ListView):
    permission_required = 'order.can_process_orders'
    model = Order
    template_name = 'order/order_list_corp.html'
    
    def get_queryset(self):
        return Order.objects.filter(corp=self.request.user.profile.pcharacter.corp).exclude(status='c')
        
class orderManageDetail(LoginRequiredMixin,PermissionRequiredMixin,generic.DetailView): #处理订单
    permission_required = 'order.can_process_orders'
    model = Order
    template_name = 'order/order_detail_manage.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs['pk']
        order = Order.objects.get(pk=pk)
        items = regularOrderUnit.objects.filter(order=order)
        stocks = []
        for i in items:
            try:
                istock = InvStorage.objects.filter(invtype=i.item).filter(corp=self.request.user.profile.pcharacter.corp).get()
            except:
                stocks.append("无库存记录")
            else:
                stocks.append(istock.stock)
        context['data'] = zip(items,stocks)
        return context
        
@permission_required('order.can_process_orders')
@transaction.atomic
@login_required
def update_orderunit(request,pk):
    ou = regularOrderUnit.objects.get(pk=pk)
    order = Order.objects.get(pk=ou.order_id)
    order.totalprice -= ou.price * ou.quantity
    
    if request.POST.get('price'):
        ou.price = int(request.POST.get('price'))
    if request.POST.get('quantity'):
        ou.quantity = int(request.POST.get('quantity'))
        
    try:
        ou.save()
        order.totalprice += ou.price * ou.quantity
        order.save()
    except OverflowError:
        messages.error(request,"数值过大，请拆分处理")
    
    return redirect(request.META['HTTP_REFERER'])
    
@permission_required('order.can_process_orders')
@transaction.atomic
@login_required
def complete_order(request,pk): #完成订单
    order = Order.objects.get(pk=pk)
    if order.status == 'o' or order.status == 'p':
        order.discount = request.POST.get('discount')
        itemcount = range(order.itemcount)
        itemuid = []
        stat = []
        totalprice = 0
    
        for n in itemcount:
            check = 'check' + str(n+1)
            requestitem = request.POST.get(check)
            #print(requestitem)
            try:
                itemuid.append(requestitem.split('/')[1])
            except:
                messages.error(request,"订单中有物品没有被指定操作，请确保每一件物品的“操作”栏都有一个选项是选中的。")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            else:
                stat.append(requestitem.split('/')[0])
        
        itemlist = zip(itemuid,stat)
        if 'wait' in stat:
            print("this order has a WAIT")
            order.status = 'p'
        else:
            order.status = 'f'
    
        for i in itemlist:
            uid = i[0]
            stat = i[1]
            ou = regularOrderUnit.objects.get(pk=uid)
            if stat == 'ok' or stat == 'wait':
                try:
                    stock = InvStorage.objects.filter(invtype=ou.item).filter(corp=order.corp).get()
                except:
                    pass
                else:
                    stock.stock -= ou.quantity
                    stock.updatetime = timezone.now()
                    if stock.stock < 0:
                        stock.stock = 0
                    stock.save() #更新库存数据
                totalprice += ou.price * ou.quantity
                ou.status = 's'
                ou.save() #更新条目状态
                try: # 更新销售统计
                    sell = InvStorage.objects.filter(invtype=ou.item).filter(corp=order.corp).get()
                except InvStorage.DoesNotExist:
                    sell = InvStorage(stock=0,corp=order.corp,sell=ou.quantity,invtype=ou.item)
                    sell.save()
                else:
                    sell.sell += ou.quantity
                    sell.updatetime = timezone.now()
                    sell.save()
            if stat == 'no':
                ou.status = 'e'
                ou.save()
            elif stat == 'wait':
                ou.status = 'p'
                ou.save()
        
        order.totalprice = totalprice
        order.finishdate = timezone.now()
        order.save()
        lg_group = User.objects.filter(profile__pcharacter__corp=request.user.profile.pcharacter.corp).filter(groups__id=1)
        
        if request.user.profile.nickname != None:
            rname = request.user.profile.nickname
        else:
            rname = request.user.get_username()
        
        if order.status == 'f':
            notify.send(request.user,recipient=lg_group,verb="订单{}已由{}完成".format(order.uid,rname),action_object=order)
            notify.send(request.user,recipient=order.user,verb="{}完成了你的订单{}，请在游戏内查看合同".format(rname,order.uid),action_object=order)
        if order.status == 'p':
            notify.send(request.user,recipient=lg_group,verb="订单{}已由{}更新".format(order.uid,rname),action_object=order)
            notify.send(request.user,recipient=order.user,verb="{}正在处理你的订单{}，有部分物品延时发货，请在游戏内查看合同".format(rname,order.uid),action_object=order)
        return render(request,'order/complete_order.html')
    else:
        messages.error(request,"该订单已完成")
        return redirect('order-list-corp')
    
    
    
    
    
    
    
    
    
    
    