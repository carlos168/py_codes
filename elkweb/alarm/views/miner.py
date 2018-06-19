# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from alarm.models import Miner
import json
from django.core import serializers


# Create your views here.

@csrf_exempt
@require_http_methods(["POST"])
def Add(request):
    '''
    http://localhost:8000/api/miner/add?name=test
    curl -H 'Content-Type: application/json' -X POST -d '{"name": "test2"}' localhost:8000/api/miner/add
    curl -X POST 'localhost:8000/api/miner/add'  -d 'name=test3'
    '''
    response = {}
    try:
        req = json.loads(request.body)
        miner_list = Miner.objects.filter(name__icontains=req['name'])
        print miner_list
        if len(miner_list) > 0:
            response['msg'] = '%s is exist' % req['name']
            response['error_num'] = 1
        else:
            # print req['name']
            # print request.POST.get('name')
            miner = Miner(name=req['name'])
            miner.save()
            response['msg'] = 'success'
            response['error_num'] = 0
    except  Exception,e:
        response['msg'] = str(e)
        response['error_num'] = 1

    return JsonResponse(response)



@require_http_methods(["GET"])
def List(request):
    '''
    http://localhost:8000/api/miner/list
    '''
    response = {}
    try:
        miners = Miner.objects.filter()
        response['list']  = json.loads(serializers.serialize("json", miners))
        response['msg'] = 'success'
        response['error_num'] = 0
    except  Exception,e:
        response['msg'] = str(e)
        response['error_num'] = 1

    return JsonResponse(response)

