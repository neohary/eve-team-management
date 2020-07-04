from .models import Cart
from django.contrib.auth.decorators import login_required
import requests

def get_user_cart_count(request):
    if request.user.is_authenticated:
        count = Cart.objects.filter(client=request.user).count()
        return {'user_cart_count':count}
    else:
        count = 0
        return {'user_cart_count':count}