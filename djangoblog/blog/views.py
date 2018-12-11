from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy

from .models import Author, Blog
from django.views import generic
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView


# Create your views here.
#def index(request):
#    return render(request, 'index.html')

class Index(LoginRequiredMixin, generic.ListView):
    model = Blog
    paginate_by = 5
    template_name = 'index.html'

    def get_queryset(self):
        return Blog.objects.filter(author__user=self.request.user).order_by('-post_date')


class BlogListView(generic.ListView):
    model = Blog
    paginate_by = 5


class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 5


class BlogDetailView(generic.DetailView):
    model = Blog


class BlogListbyAuthorView(generic.ListView):
    model = Blog
    paginate_by = 5
    template_name = 'blog/blog_list_by_author.html'

    def get_queryset(self):
        id = self.kwargs['pk']
        target_author = get_object_or_404(Author, pk = id)
        return Blog.objects.filter(author=target_author)

    def get_context_data(self, **kwargs):
        context = super(BlogListbyAuthorView, self).get_context_data(**kwargs)
        id = self.kwargs['pk']
        author = get_object_or_404(Author, pk = id)
        context['author'] = author
        if author.following.filter(user=self.request.user).exists():
            context['is_followed'] = True
        else:
            context['is_followed'] = False
        return context


class BlogCreate(LoginRequiredMixin, CreateView):
    model = Blog
    fields = ['title', 'text']

    def form_valid(self, form):
        form.instance.author = Author.objects.get(user=self.request.user)
        return super(BlogCreate, self).form_valid(form)


class Feed(LoginRequiredMixin,generic.ListView):
    model = Blog
    paginate_by = 5
    template_name = 'blog/feed_list.html'

    def get_queryset(self):
        return Blog.objects.filter(author__following__user=self.request.user).\
            exclude(readedby__user=self.request.user)


def follow_author(request, pk):
    author_to_follow = get_object_or_404(Author, pk=pk)
    author__user = request.user
    data = {}
    author_to_follow.following.add(Author.objects.get(user=author__user))
    return JsonResponse(data={}, safe=False)

def unfollow_author(request, pk):
    author_to_unfollow = get_object_or_404(Author, pk=pk)
    author_user = request.user
    author_to_unfollow.following.remove(Author.objects.get(user=author_user))
    readers = Author.objects.get(user=author_user)
    for i in Blog.objects.filter(author__user=author_to_unfollow.user, readedby__user=author_user):
        readers.readed.remove(i)

    return JsonResponse(data={}, safe=False)

def markAsRead(request, pk):
    blog_as_read = get_object_or_404(Blog, pk=pk)
    readedby = request.user
    blog_as_read.readedby.add(Author.objects.get(user=readedby))
