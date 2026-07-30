from django.shortcuts import render
from article.models import Post, Category                    

def home(request):
    posts = Post.objects.all()
    return render(request, "home/index.html", {'posts': posts})

# Create your views here.
