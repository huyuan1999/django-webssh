from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django_webssh.tools import tools
import json



def index(request):
    if request.method == 'GET':
        return render(request, 'index.html')

    elif request.method == 'POST':
        success = {'code': 0, 'message': None, 'error': None}

        try:
            post_data = request.POST.get('data')
            data = json.loads(post_data)

            auth = data.get('auth')
            if auth == 'key':
                pkey = request.FILES.get('pkey')
                key_content = pkey.read().decode('utf-8')
                data['pkey'] = key_content
            else:
                data['password'] = data.get('password')

            unique = tools.unique()
            data['unique'] = unique

            valid_data = tools.ValidationData(data)

            if valid_data.is_valid():
                valid_data.save()
                success['message'] = unique
            else:
                error_json = valid_data.errors.as_json()
                success['code'] = 1
                success['error'] = error_json

            return JsonResponse(success)
        except:
            success['code'] = 1
            success['error'] = '发生未知错误'
            return JsonResponse(success)
