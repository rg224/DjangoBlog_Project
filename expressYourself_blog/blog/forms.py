from django import forms
from blog.models import Post, Comment

class PostForm(forms.ModelForm):

    class Meta:
        model = Post # connecting with the model we want to use
        fields = ('author', 'title', 'text') # fields we want to edit

        # adding widgets to make form more styled
        widgets = {
            # 'author':forms.TextInput(attrs={'class':'textinputclass'}), # <lablel>Author:</label> <input type = "text" class = "textinputclass">
            'title':forms.TextInput(attrs={'class':'textinputclass'}),
            'text':forms.Textarea(attrs={'class':'editable medium-editor-textarea postcontent'})
        }

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('author', 'text')

        widgets = {
            'author':forms.TextInput(attrs={'class':'textinputclass'}),
            'text':forms.Textarea(attrs={'class':'editable medium-editor-textarea'})
        }
