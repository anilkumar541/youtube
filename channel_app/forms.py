from django import forms
from coreapp.models import Video
from channel_app.models import Community





class VideoForm(forms.ModelForm):
    title= forms.CharField(widget=forms.TextInput(attrs={"id": "title", "onkeyup": "titleValidate()"}))
    description= forms.CharField(widget=forms.Textarea(attrs={"id": "description", "onkeyup": "desc_validate()"}))
    image= forms.ImageField(widget=forms.FileInput(attrs={"class": "file", "onkeyup": "desc_validate()"}))
    video= forms.FileField(widget=forms.FileInput(attrs={"class": "file", "onkeyup": "desc_validate()"}))
    

    class Meta:
        model= Video
        fields= ["video", "image", "title", "description", "tags", "visibility"]

class CommunityForm(forms.ModelForm):

    class Meta:
        model= Community
        fields= ["content", "image"]