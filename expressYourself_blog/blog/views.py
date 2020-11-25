from django.shortcuts import render
from blog.models import Post, Comment
from blog.forms import PostForm, CommentForm
from django.views.generic import (TemplateView, ListView, 
                                  DetailView, CreateView,
                                  UpdateView, DeleteView)
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy # it waits until you've actually deleted it to redirect you to someother page

# Create your views here.

class AboutView(TemplateView):
    template_name = 'about.html'

# it will be the homepage that shows list of posts
class PostListView(ListView):
    model = Post
    # template_name = 'post_list.html'

    def get_queryset(self): # this method allows us to use Django's ORM (Object Relational Mapping)
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')

# this will show detail of particular post        
class PostDetailView(DetailView):
    model = Post

# since we want only particular person to create post according to his or her login
class CreatePostView(LoginRequiredMixin, CreateView):
    # attributes of LoginRequiredMixin
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'
    form_class = PostForm
    
    model = Post

class PostUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'
    form_class = PostForm
    
    model = Post

class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('post_list')

# it will all the posts which are not yet published i.e. their published_date = NULL
class DraftListView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_list.html'

    model = Post

    def get_queryset(self):
        return Post.objects.filter(published_date__isnull=True).order_by('created_date')