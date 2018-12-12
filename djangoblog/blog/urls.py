from django.urls import path

from . import views


urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('blogs/', views.BlogListView.as_view(), name='blogs'),
    path('authors/', views.AuthorListView.as_view(), name='authors'),
    path('blog/<int:pk>', views.BlogDetailView.as_view(), name='blog-detail'),
    path('author/<int:pk>', views.BlogListbyAuthorView.as_view(), name='blogs-by-author'),
    path('blog/create/', views.BlogCreate.as_view(), name='blog-create'),
    path('follow/<int:pk>', views.follow_author, name='follow-author'),
    path('unfollow/<int:pk>', views.unfollow_author, name='unfollow-author'),
    path('feed/', views.Feed.as_view(), name='feed'),
    path('readed/<int:pk>', views.mark_as_read, name='mark-as-read'),

]
