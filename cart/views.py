from django.shortcuts import render
from .models import Cart
from sde.models import Invtypes
from sde.forms import add_CartFrom
from corp.models import EveCharacter
import requests
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.http import JsonResponse
import xmltodict
from django.contrib.auth.decorators import permission_required
from django.contrib import messages
from django.db import transaction
from django.core.exceptions import PermissionDenied
# Create your views here.

@permission_required('cart.user_can_use_cart')
@transaction.atomic
@login_required
def myCartListView(request):
    if request.user:
        carts = Cart.objects.filter(client=request.user)
        characters = EveCharacter.objects.filter(bounduser=request.user)
        sumprices = []
        for cart in carts:
            url = 'https://www.ceve-market.org/api/marketstat?typeid={0}&usesystem=30000142'.format(cart.item.typeid)
            response = requests.get(url)
            data = xmltodict.parse(response.content)['evec_api']['marketstat']['type']['sell']['percentile']
            if cart.price != int(data.split('.')[0]):
                cart.price = float(data)
                cart.save()
            sumprices.append(cart.quantity * float(data))
        context = {
            "data":zip(carts,sumprices),
            "totalprice":sum(sumprices),
            "charselect":characters,
        }
    return render(request,'cart/my_cart.html',context)
    
@permission_required('cart.user_can_use_cart')
@login_required
@transaction.atomic
def delete_cart(request,pk):
    try:
        record = Cart.objects.get(pk=pk)
    except Cart.DoesNotExist:
        messages.error(request,"指定的记录不存在")
    else:
        if request.user == record.client:
            record.delete()
            return redirect('my-cart')
        else:
            raise PermissionDenied
    

@permission_required('cart.user_can_use_cart')
@login_required
@transaction.atomic
def add_cart(request,item):
    if request.is_ajax():
        count = Cart.objects.filter(client=request.user).count()
        if count >= 16:
            return JsonResponse({'msg':"添加失败 购物车已达上限"})
        else:
            quantity = request.POST.get('quantity',None)
            p_temp = request.POST.get('price',None)
            price = p_temp.split('.')[0]
            carts = Cart.objects.filter(client=request.user,item_id=item)
            if carts.exists():
                cart = carts[0]
                cart.quantity += int(quantity)
                cart.price = price
            else:
                cart = Cart(client=request.user,item_id=item,quantity=quantity,price=price)
            cart.save()
            return JsonResponse({'msg':"已添加到购物车"})
    else:
        return redirect('my-cart')
        
def update_cart(request,pk):
    try:
        record = Cart.objects.get(pk=pk)
    except Cart.DoesNotExist:
        messages.error(request,"指定的记录不存在")
    else:
        if request.user == record.client:
            if request.POST.get('quantity'):
                record.quantity = int(request.POST.get('quantity'))
                record.save()
                messages.success(request,"记录更新成功")
                return redirect('my-cart')
        else:
            raise PermissionDenied
    
    
    
    
    
    
    
    
    