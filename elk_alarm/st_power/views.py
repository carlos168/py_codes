# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
from django.shortcuts import render

# from st_power.models import st_power

# Create your views here.

def  list(request):
    List = ['自强学堂', '渲染Json到模板']
    Dict = {'site': '自强学堂', 'author': '涂伟忠'}
    context = {
        'List': json.dumps(List),
        'Dict': json.dumps(Dict)
    }
    return render(request, 'list.html', context)