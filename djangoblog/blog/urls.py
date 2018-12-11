from django.conf.urls import url
from django.urls import path

from . import views


urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('blogs/', views.BlogListView.as_view(), name='blogs'),
    path('authors/', views.AuthorListView.as_view(), name='authors'),
    path('blog/<int:pk>', views.BlogDetailView.as_view(), name='blog-detail'),
    path('author/<int:pk>', views.BlogListbyAuthorView.as_view(), name='blogs-by-author'),

]
