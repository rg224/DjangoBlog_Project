from django.db import models
from django.utils import timezone
from django.urls import reverse

# Create your models here.

class Post(models.Model):

    # on_delete = models.CASCADE means that when the referenced object is deleted, also delete the objects that have refernces to it.
    # (when you remove a blog post for instance, you might want to delete comments as well)
    # It is more specifically SQL standard

    author = models.ForeignKey('auth.User', on_delete=models.CASCADE) # superuser will eventually become author
    title = models.CharField(max_length=200)
    text = models.TextField()
    create_date = models.DateTimeField(default = timezone.now)
    published_date = models.DateTimeField(blank=True,null=True)

    def __str__(self):
        return self.title # or return "{}".format(title)

    def publish(self): # on hitting the publish button it will set published_date's timezone 
        self.published_date = timezone.now()
        self.save()

    # get_absolute_url() method is used so that on creating a post, when you hit publish button it will take you to a post_detail page showing the post you created (pk).
    def get_absolute_url(self): # get_absolute_url is default method name django looks for actually
        return reverse('post_detail', kwargs={'pk':self.pk})

    def approve_comments(self):
        return self.comments.filter(approved_comment = True) # it says that show all the comments under the respective post that are set to True (approved)


class Comment(models.Model):
    post = models.ForeignKey('blog.Post', related_name='comments', on_delete=models.CASCADE) # it will connect each comment to actual post
    author = models.CharField(max_length=200) # this author is someone who wrote the comment
    text = models.TextField()
    create_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def get_absolute_url(self):
        return reverse('post_list')

    def __str__(self):
        return self.text