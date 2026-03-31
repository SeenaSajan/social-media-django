from django import forms
from .models import Post, Story
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['image', 'caption']
        widgets = {
            'caption': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Write a caption...'
            }),
        }

class StoryForm(forms.ModelForm):
    class Meta:
        model = Story
        fields = ['image']