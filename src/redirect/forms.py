from django import forms
from redirect.models import ShortLink


ALLOWED_CHARS = set('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_')

class ShortLinkForm(forms.ModelForm):
    class Meta:
        model = ShortLink
        fields = ['code', 'url']

    def clean_code(self):
        code = self.cleaned_data.get('code')
        if not all(c in ALLOWED_CHARS for c in code):
            raise forms.ValidationError('Only letters, numbers, hyphens and underscores are allowed.')
            
        return code
