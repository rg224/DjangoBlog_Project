from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from blog.models import Post, Comment
from blog.forms import PostForm, CommentForm

from django.views.generic import (TemplateView, ListView, 
                                  DetailView, CreateView,
                                  UpdateView, DeleteView)

# for authorization purpose
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

# it waits until you've actually deleted it to redirect you to someother page
from django.urls import reverse_lazy 


# Create your views here.
######################################### POST VIEWS #########################################
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
    template_name = 'post_confirm_delete.html'
    success_url = reverse_lazy('post_list')

# it will all the posts which are not yet published i.e. their published_date = NULL
class DraftListView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    template_name = 'post_draft_list.html'

    model = Post

    def get_queryset(self):
        return Post.objects.filter(published_date__isnull=True).order_by('create_date')

@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()

    return redirect('post_detail', pk=post.pk)

######################################### COMMENT VIEWS #########################################

@login_required # a person has to be LoggedIn in order to comment
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == 'POST':
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()

            return redirect('post_detail', pk=post.pk)

    else:
        form = CommentForm()
    return render(request, 'blog/comment_form.html', {'form':form})

@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve() # this approve() method is defined in models.py under model Comment

    return redirect('post_detail', pk=comment.post.pk)

@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    comment.delete()

    return redirect('post_detail', pk=post_pk)

    