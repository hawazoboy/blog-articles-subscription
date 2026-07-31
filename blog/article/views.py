from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse



def article_detail(request, slug):
    article =get_object_or_404(Post, slug=slug)
    is_liked = False

    if request.user.is_authenticated:
        is_liked = article.likes.filter(
            user=request.user
        ).exists()

    return render(request, 'article_detail.html', {'article': article, 'is_liked': is_liked})


def all_articles(request):
    all_articles = Post.objects.all().order_by("-id") 
    paginator = Paginator(all_articles, 2)
    page_number = request.GET.get('page')
    objects_list = paginator.get_page(page_number)
    return render(request, 'all_articles.html', {'all_articles': objects_list})

def category_detail(request, id):
    category_obj = get_object_or_404(Category, id=id)
    all_articles = category_obj.posts.all() 
    return render(request, 'all_articles.html', {'all_articles': all_articles})

def search_articles(request):
    q = request.GET.get('q')
    articles = Post.objects.filter(title__icontains=q)
    paginator = Paginator(articles, 2)
    page_number = request.GET.get('page')
    objects_list = paginator.get_page(page_number)
    return render(request, 'all_articles.html',  {'all_articles': objects_list})


@login_required
def like_post(request, slug):
    post = get_object_or_404(Post, slug=slug)

    liked = False

    like = PostLike.objects.filter(
        post=post,
        user=request.user
    )

    if like.exists():
        like.delete()
    else:
        PostLike.objects.create(
            post=post,
            user=request.user
        )
        liked = True

    return JsonResponse({
        "liked": liked,
        "likes_count": post.likes.count()
    })