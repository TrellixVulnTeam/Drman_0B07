from django import forms
from .models import Comments
from crispy_forms.helper import FormHelper

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False,widget=forms.Textarea)

class CommentsForm(forms.ModelForm) :
    class Meta:
        model = Comments
        fields = ('name', 'email', 'body')

class SearchForm(forms.Form) :
    search = forms.CharField(widget=forms.TextInput(attrs={'id': 'ajab',
                                                           'class': "form-control border-radius-0 direction-r blog-search-input" ,
                                                           'placeholder': "جست و جو..."}))

    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False


