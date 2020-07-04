from django.contrib.auth.models import User,Group
from .models import EveCorporation
from django.contrib.auth.decorators import login_required
import requests

def get_corp_verification_count(request):
    if request.user.is_authenticated:
        try:
            corp = request.user.profile.pcharacter.corp
        except:
            count = 0
        else:
            count = User.objects.filter(profile__pcharacter__corp=corp).filter(groups__id=5).count()
        return {'corp_verification_count':count}
    else:
        count = 0
        return {'corp_verification_count':count}