"""Django form, used for html form submission"""

from django import forms
from .models import Wizbulb


class BulbForm(forms.ModelForm):
    """ "Form used to create and edit bulbs in the database"""

    bulb_name = forms.CharField(max_length=50)
    bulb_ip = forms.CharField(max_length=16)
    bulb_state = forms.BooleanField(required=False)
    bulb_red = forms.IntegerField(required=False)
    bulb_green = forms.IntegerField(required=False)
    bulb_blue = forms.IntegerField(required=False)
    bulb_temp = forms.IntegerField(required=False)

    def __init__(self, *args, **kwargs):
        super(BulbForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"

    class Meta:
        """Meta class for the form, used to set the model and fields"""

        model = Wizbulb
        fields = "__all__"
        widgets = {
            "bulb_ip": forms.HiddenInput(),
            "bulb_state": forms.HiddenInput(),
            "bulb_red": forms.HiddenInput(),
            "bulb_green": forms.HiddenInput(),
            "bulb_blue": forms.HiddenInput(),
            "bulb_temp": forms.HiddenInput(),
        }
