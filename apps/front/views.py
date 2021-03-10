from django.shortcuts import render
import uuid

def all_articles(request):
    return render(request, 'layouts/main.html', {
        "CHANNEL": uuid.uuid4().hex[:20].upper()
        })
