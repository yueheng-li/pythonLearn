# -*- coding: utf-8 -*-
 
from django.http import HttpResponse
from django.shortcuts import render_to_response
from app_name.models import Test
 
# 表单
def search_form(request):
	
    return render_to_response('search_form.html')
 
# 接收请求数据
def search(request):  
    if 'q' in request.GET:
        message = '你搜索的内容为: ' + request.GET['q']
    else:
        message = '你提交了空表单'
    return HttpResponse(message)