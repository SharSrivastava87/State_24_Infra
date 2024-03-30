from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
import json
def dashboard(request):
    return render(request, 'dashboard.html')

def sign_in(request):
    return render(request, 'sign-in.html')

def sign_up(request):
    return render(request, 'sign-up.html')

def presentation(request):
    return render(request, 'tables.html')

def update_time_range(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        time_range = data['timeRange']
        return JsonResponse({'status': 'success', 'time_range': time_range})