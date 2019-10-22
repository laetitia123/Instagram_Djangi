from django import forms

from .models import *


class Post_image_Form(forms.Form):
    class Meta:
         model=Image
         exclude=('user',)

class ProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['Name'].widget = forms.TextInput()

    class Meta:
        model = Profile
        fields = ('Name', 'profile_picture', 'bio')
        # exclude=['user']


# class PostForm(forms.ModelForm):
#     class Meta:
#         model = Image
#         exclude = ('user', )


# class ProfileForm(forms.ModelForm):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['Name'].widget = forms.TextInput()

#     class Meta:
#         model = Profile
#         fields = ('Name', 'profile_picture', 'bio')


class CommentForm(forms.ModelForm):
  
    class Meta:
        model = Comment
        fields = ('comment',)

class NewsLetterForm(forms.Form):
    your_name = forms.CharField(label='First Name',max_length=30)
    email = forms.EmailField(label='Email')


class NewsLetterForm(forms.Form):
    your_name = forms.CharField(label='First Name',max_length=30)
    email = forms.EmailField(label='Email')
class uploadimageForm(forms.ModelForm):
    class Meta:
        model = Image
        exclude = ['editor', 'pub_date']
        widgets = {
            'tags': forms.CheckboxSelectMultiple(),
        }
class uploadimageForm(forms.ModelForm):
    class Meta:
        model = Image
        exclude = ['editor', 'pub_date']
        widgets = {
            'tags': forms.CheckboxSelectMultiple(),
        }        