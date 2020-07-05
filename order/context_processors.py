from django.contrib.auth.models import User
from .models import Order
from corp.models import EveCorporation
from django.contrib.auth.decorators import login_required
import requests
from django.db.models import Q

def get_user_ongoing_orders_count(request):
    if request.user.is_authenticated:
        count = Order.objects.filter(user=request.user).filter(status='o').count()
        return {'user_ongoing_orders_count':count}
    else:
        count = 0
        return {'user_ongoing_orders_count':count}
        
def get_corp_ongoing_orders_count(request):
    if request.user.is_authenticated:
        try:
            corp = request.user.profile.pcharacter.corp
        except:
            count = 0
        else:
            count = Order.objects.filter(corp=corp).filter(Q(status='o') | Q(status='p')).count()
        return {'corp_ongoing_orders_count':count}
    else:
        count = 0
        return {'corp_ongoing_orders_count':count}