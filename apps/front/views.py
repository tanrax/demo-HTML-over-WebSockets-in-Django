from django.shortcuts import render
from apps.back.models import Post
import uuid

def all_articles(request):
    return render(request, 'layouts/main.html', {
        "CHANNEL": uuid.uuid4().hex[:20].upper(),
        "posts": Post.objects.all()[:3],
        "pag": 1
        })
