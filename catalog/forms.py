from django import forms

from .models import AppStatus


class AppStatusForm(forms.ModelForm):
    class Meta:
        model = AppStatus
        fields = ['name', 'color', 'description']
        widgets = {
            'color': forms.TextInput(attrs={'type': 'color'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }
