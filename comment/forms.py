from django import forms
from .models import Comment
from django.core.exceptions import ValidationError


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'url', 'text']

    def clean_name(self):
        value = self.cleaned_data.get('name')
        if '屏蔽' in value:
            raise ValidationError('屏蔽不能在name中')
        else:
            return value

