from django.forms import ModelForm
from django import forms
from .models import Blog

class BlogForm(ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'featured_image','category', 'summary', 'content', 'draft']
        widgets = {
            'category': forms.RadioSelect(),
        }

    def __init__(self, *args, **kwargs):
        super(BlogForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})