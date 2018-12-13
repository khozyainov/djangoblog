from django.urls import path

from . import views


urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('blogs/', views.BlogListView.as_view(), name='blogs'),
    path('blog/<int:pk>', views.BlogDetailView.as_view(), name='blog-detail'),
    path('blog/<int:pk>/readed', views.mark_as_read, name='mark-as-read'),
    path('blog/create/', views.BlogCreate.as_view(), name='blog-create'),
    path('authors/', views.AuthorListView.as_view(), name='authors'),
    path('author/<int:pk>', views.BlogListbyAuthorView.as_view(), name='blogs-by-author'),
    path('author/<int:pk>/follow', views.follow_author, name='follow-author'),
    path('author/<int:pk>/unfollow', views.unfollow_author, name='unfollow-author'),
    path('feed/', views.Feed.as_view(), name='feed'),

]
