from django import forms
from .models import wizbulb


class bulbForm(forms.ModelForm):
    bulbName = forms.CharField(max_length=50)
    bulbIp = forms.CharField(max_length=16)
    bulbState = forms.BooleanField(required=False)
    bulbRed = forms.IntegerField(required=False)
    bulbGreen = forms.IntegerField(required=False)
    bulbBlue = forms.IntegerField(required=False)
    bulbTemp = forms.IntegerField(required=False)

    def __init__(self, *args, **kwargs):
        super(bulbForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = wizbulb
        fields = "__all__"
        widgets = {
            "bulbIp": forms.HiddenInput(),
            "bulbState": forms.HiddenInput(),
            "bulbRed": forms.HiddenInput(),
            "bulbGreen": forms.HiddenInput(),
            "bulbBlue": forms.HiddenInput(),
            "bulbTemp": forms.HiddenInput(),
        }
