from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from PIL import Image
from io import BytesIO
import base64


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


# Helper
def image_to_base64(image):
    buff = BytesIO()
    image.save(buff, format="PNG")
    img_str = base64.b64encode(buff.getvalue())
    img_str = img_str.decode("utf-8")  # convert to str and cut b'' chars
    return img_str


def visualize_data(request, hour):
    image = Image.open(f'plumes/plume{hour}.png')
    image64 = image_to_base64(image)
    return render(request, 'visualization.html', {'plume': image64})
    