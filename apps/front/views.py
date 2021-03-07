from django.shortcuts import render

def blog(request):
    return render(request, 'blog.html')
