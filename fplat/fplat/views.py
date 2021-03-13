from django.shortcuts import render

def home(request):
    return render(request, 'home.html', {})

def articles(request):
    return render(request, 'articles.html', {})