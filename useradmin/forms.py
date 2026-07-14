from django import forms

from catalog.models import AppLink


def managed_app_choices():
    apps = [a for a in AppLink.objects.all() if a.user_management_enabled]
    return [(a.pk, a.name) for a in apps]


class UserCreateForm(forms.Form):
    app = forms.ChoiceField(label='App')
    username = forms.CharField(max_length=150)
    email = forms.EmailField(required=False)
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['app'].choices = managed_app_choices()


class UserUpdateForm(forms.Form):
    email = forms.EmailField(label='Email', required=False)
    is_active = forms.BooleanField(label='Attivo', required=False)
    new_password = forms.CharField(
        label='Nuova password', required=False, widget=forms.PasswordInput,
        help_text='Lascia vuoto per non cambiarla.',
    )
