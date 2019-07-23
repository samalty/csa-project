from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['subject', 'feedback', 'mentorship', 'hiring', 'community', 'fundraising', 'corporate_dev']

class RawReviewForm(forms.Form):
    RATINGS = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
    )
    subject = forms.CharField(label='Subject', 
                                widget=forms.TextInput(
                                    attrs={
                                        "placeholder":"What company are you reviewing?",
                                    }))
    feedback = forms.CharField(
                    label='', 
                    widget=forms.Textarea(
                        attrs={
                            'cols': 80,
                        }))
    mentorship = forms.ChoiceField(widget=forms.RadioSelect, choices=RATINGS)
    hiring = forms.ChoiceField(widget=forms.RadioSelect, choices=RATINGS)
    community = forms.ChoiceField(widget=forms.RadioSelect, choices=RATINGS)
    fundraising = forms.ChoiceField(widget=forms.RadioSelect, choices=RATINGS)
    corporate_dev = forms.ChoiceField(widget=forms.RadioSelect, choices=RATINGS)
