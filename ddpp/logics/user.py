#-*- coding: utf-8 -*-
import json
import pprint
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from ddpp.common.utils import BID_BASE, check_bid_vaild
#from rest_framework.decorators import api_view

def test(request):
    data = {}
    data['rc'] = 1
    data['order_id'] = ''

    return HttpResponse(
                json.dumps(data, indent=1),
                content_type='application/x-javascript',
            )

@csrf_exempt
def get_tender(request):

    if request.method == 'GET':
        params = dict(request.GET)
    else:
        params = dict(request.POST)

    tender = params.get('tender', '')
    idcard = params.get('idcard', '')
    if not ( tender and idcard ):
        data = {}
        data['data'] = {}
        data['result'] = -1
    else:
        if len(idcard[0]) != 4:
            idcard = idcard[0][-4:]
        else:
            idcard = idcard[0]
        tender = tender[0]
        result, data = BID_BASE().check_bid(tender, idcard)
        data['result'] = result
    return HttpResponse(
                json.dumps(data, indent=1),
                content_type='application/x-javascript',
            )

@csrf_exempt
def bid_vaild(request):

    if request.method == 'GET':
        params = dict(request.GET)
    else:
        params = dict(request.POST)

    phone = params.get('phone', '')
    idcard = params.get('idcard', '')
    data = {}
    if not ( phone and idcard ):
        data['data'] = {}
        data['result'] = -1
    else:
        idcard = idcard[0]
        phone = phone[0]
        result, info = check_bid_vaild(idcard, phone)
        data['result'] = result
        data['data'] = info
    return HttpResponse(
                json.dumps(data, indent=1),
                content_type='application/x-javascript',
            )