#-*- coding: utf-8 -*-
import json
from django.http import HttpResponse


def test(request):
    data = {}
    data['rc'] = 1
    data['order_id'] = ''

    return HttpResponse(
                json.dumps(data, indent=1),
                content_type='application/x-javascript',
            )