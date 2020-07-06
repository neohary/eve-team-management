from django.shortcuts import render
from .models import Eveicons,Invtypes,Marketgroups
from corp.models import InvStorage
from django.http import HttpResponse
from django.views.decorators.clickjacking import xframe_options_exempt
import requests
import xmltodict
from django.contrib.auth.decorators import permission_required,login_required
from django.db import transaction
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.views.decorators.cache import cache_page
# Create your views here.
    
@permission_required('sde.user_can_use_market')
def show_marketgroups(request):

        

    return render(request,"sde/marketgroups.html",{'marketgroups':Marketgroups.objects.all()})
    
from django.views import generic

class itemListView(generic.ListView):
    model = Invtypes
    template_name = 'sde/invtypes_list.html'
    
    @transaction.atomic
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs['pk']
        invtypes = Invtypes.objects.filter(marketgroupid=pk).order_by('typeid')
        ls = Invtypes.objects.values_list('typeid',flat=True).filter(marketgroupid=pk).order_by('typeid')
        prices = []
        stock = []
        for l in ls:
            url = 'https://www.ceve-market.org/api/marketstat?typeid={0}&regionlimit=10000002'.format(l)
            response = requests.get(url)
            data = xmltodict.parse(response.content)['evec_api']['marketstat']['type']['sell']['percentile']
            try:
                prices.append(data)
            except UnboundLocalError:
                prices.append("错误")
                
            try:
                stockinv = InvStorage.objects.filter(corp_id=self.request.user.profile.pcharacter.corp_id).get(invtype_id=l) #corp_id = 接入的库存数据
            except InvStorage.DoesNotExist:
                stock.append(0)
            else:
                stock.append(stockinv.stock)
        context['data'] = zip(invtypes,prices,stock)
        return context
        
from django.template.loader import render_to_string
from django.http import JsonResponse

@transaction.atomic
def itemListSearchView(request):
    context = {}
    url_parameter = request.GET.get('q')
    if url_parameter:
        invtypes = Invtypes.objects.filter(published=1).filter(marketgroupid__isnull=False).filter(typename__icontains=url_parameter).order_by('typeid')
        ls = Invtypes.objects.values_list('typeid',flat=True).filter(published=1).filter(marketgroupid__isnull=False).filter(typename__icontains=url_parameter).order_by('typeid')
        stock = []
        prices = []
        for l in ls:
            url = 'https://www.ceve-market.org/api/marketstat?typeid={0}&regionlimit=10000002'.format(l)
            response = requests.get(url)
            data = xmltodict.parse(response.content)['evec_api']['marketstat']['type']['sell']['percentile']
            
            try:
                prices.append(data)
            except UnboundLocalError:
                prices.append("错误")
            
            try:
                stockinv = InvStorage.objects.filter(corp_id=request.user.profile.pcharacter.corp_id).get(invtype_id=l) #corp_id = 接入的库存数据
            except InvStorage.DoesNotExist:
                stock.append(0)
            else:
                stock.append(stockinv.stock)
    else:
        invtypes = ''
    if request.is_ajax():
        html = render_to_string(
            template_name="sde/invtypes_list.html",
            context={"data":zip(invtypes,prices,stock)},
            request=request
        )
        data_dict = {"html_from_view":html}
        
        return JsonResponse(data=data_dict,safe=False)
        
    return render(request,"sde/invtypes_list.html",context)
    
class invtypeListView(LoginRequiredMixin,generic.ListView):
    model = Invtypes
    paginate_by = 50
    template_name = 'sde/item_list.html'
    
@login_required
@transaction.atomic
def delete_all_sde_data(request):
    if request.user.is_superuser:
        invtypes = Invtypes.objects.all()
        marketgroups = Marketgroups.objects.all()
        eveicons = Eveicons.objects.all()
        invtypes.delete()
        marketgroups.delete()
        eveicons.delete()
    else:
        raise PermissionDenied
        
    return render(request,"sde/dropresult.html")