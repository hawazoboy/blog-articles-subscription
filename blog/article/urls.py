from django.urls import path
from . import views

app_name = 'article'
urlpatterns = [
    path('detail/<slug:slug>', views.article_detail, name='detail'),
    path('all_articles', views.all_articles, name='all_articles'),
    path('category/<int:id>/', views.category_detail, name='category_detail'),
    path('search/', views.search_articles, name='search_articles'),
    path('<slug:slug>/like/', views.like_post, name='like_post'),
]