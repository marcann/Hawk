# TODO:50 write forms for easy blog post submissions and editing
from django import forms
from .models import Post

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text')


class PostDeleteForm(forms.ModelForm):

    confirm = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label="Confirm Delete")

    class Meta:
        model = Post
        fields = ('confirm',)

    def clean(self):
        keyword = "delete"
        if (self.cleaned_data['confirm'].lower() != keyword):
            raise forms.ValidationError("Did not type in proper keyword.")
        return self.cleaned_data
