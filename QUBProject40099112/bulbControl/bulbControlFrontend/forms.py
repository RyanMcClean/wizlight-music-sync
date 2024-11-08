from django import forms
from .models import wizBulb

class bulbForm(forms.ModelForm):
    bulbState = forms.BooleanField(required=False)
    bulbRed = forms.IntegerField(required=False)
    bulbGreen = forms.IntegerField(required=False)
    bulbBlue = forms.IntegerField(required=False)
    bulbTemp = forms.IntegerField(required=False)
    class Meta:
        model = wizBulb
        fields = "__all__"
        widgets = {
            'bulbIp': forms.HiddenInput(),
            'bulbState': forms.HiddenInput(),
            'bulbRed': forms.HiddenInput(),
            'bulbGreen': forms.HiddenInput(),
            'bulbBlue': forms.HiddenInput(),
            'bulbTemp': forms.HiddenInput(),
        }
        

