from django import forms
from django.forms import ModelForm, Textarea
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['title', 'feedback', 'mentorship', 'hiring', 'community', 'fundraising', 'corporate_dev']
        widgets = {
            'title': Textarea(attrs={'cols': 80, 'rows': 1}),
            'feedback': Textarea(attrs={'cols': 80, 'rows': 15}),
            'mentorship': forms.RadioSelect,
            'hiring': forms.RadioSelect,
            'community': forms.RadioSelect,
            'fundraising': forms.RadioSelect,
            'corporate_dev': forms.RadioSelect,
        }