from django.shortcuts import render

def dashboard(request):
    return render(request, 'dashboard.html')

def sign_in(request):
    return render(request, 'sign-in.html')

def sign_up(request):
    return render(request, 'sign-up.html')

def presentation(request):
    return render(request, 'tables.html')