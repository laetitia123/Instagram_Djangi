from django import forms

from .models import *


class Post_image_Form(forms.Form):
    class Meta:
         model=Image
         exclude=('user',)
class ProfileForm(forms.Form):
    
    class Meta:
        model = Profile
        fields = ('Name', 'profile_picture', 'bio')

class CommentForm(forms.ModelForm):
  
    class Meta:
        model = Comment
        fields = ('comment',)



class uploadimageForm(forms.ModelForm):
    class Meta:
        model = Image
        exclude = ['editor', 'pub_date']
        widgets = {
            'tags': forms.CheckboxSelectMultiple(),
        }        