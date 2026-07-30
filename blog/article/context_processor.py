from article.models import Post, Category




def global_sidebar_data(request):
    return {
        'updated_posts': Post.objects.order_by('-created')[:3],
        'categories': Category.objects.all(),
        'recent_posts' : Post.objects.all().order_by('-created')[:3]
    }