from .models import generalInfo

def get_sitetitle(request):
    try:
        title = generalInfo.objects.get(id=1).siteTitle
    except:
        return {'title':"圈圈后勤系统"}
    else:
        return {'title':title}
    
def get_subTitle(request):
    try:
        subTitle = generalInfo.objects.get(id=1).subTitle
    except:
        return {'subTitle':"EVE团队管理平台"}
    else:
        return {'subTitle':subTitle}

def get_headInfo(request):
    try:
        headInfo = generalInfo.objects.get(id=1).headInfo
    except:
        return {'footInfo':None}
    else:
        return {'headInfo':headInfo}
		
def get_footInfo(request):
    try:
        footInfo = generalInfo.objects.get(id=1).footInfo
    except:
        return {'footInfo':"©版权所有 NeoHary 由DJANGO强力驱动"}
    else:
        return {'footInfo':footInfo}

def get_version(request):
    try:
        version = generalInfo.objects.get(id=1).version
    except:
        return {'version':"v1.0"}
    else:
        return {'version':version}

def is_inviteRegOnly(request):
    try:
        inviteRegOnly = generalInfo.objects.get(id=1).inviteRegOnly
    except:
        return {'inviteRegOnly':False}
    else:
        return {'inviteRegOnly':inviteRegOnly}

def is_underMaintaining(request):
    try:
        underMaintaining = generalInfo.objects.get(id=1).underMaintaining
    except:
        return {'underMaintaining':False}
    else:
        return {'underMaintaining':underMaintaining}