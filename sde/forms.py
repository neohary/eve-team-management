from django import forms

class add_CartFrom(forms.Form):
    quantity = forms.IntegerField(initial=1)