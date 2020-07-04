from django import template
from sde.models import Marketgroups,Eveicons

register = template.Library()

@register.filter(name='market_icon')
def market_icon(iconid): 
    try:
        icon = Eveicons.objects.get(iconid=iconid)
    except Eveicons.DoesNotExist:
        icon = Eveicons.objects.get(iconid=0)
        
    return icon