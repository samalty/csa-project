from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['subject', 'feedback', 'mentorship', 'hiring', 'community', 'fundraising', 'corporate_dev']

RATINGS = ['1', '2', '3', '4', '5']

class RawReviewForm(forms.Form):
    #RATINGS = [
    #    ('1', '1'),
    #    ('2', '2'),
    #    ('3', '3'),
    #    ('4', '4'),
    #    ('5', '5'),
    #]
    subject = forms.CharField(label='')
    feedback = forms.CharField(
                    label='', 
                    widget=forms.Textarea(
                        attrs={
                            'cols': 80,
                        }))
    mentorship = forms.ChoiceField(widget=forms.RadioSelect(choices=RATINGS))
    hiring = forms.ChoiceField(widget=forms.RadioSelect(choices=RATINGS))
    community = forms.ChoiceField(widget=forms.RadioSelect(choices=RATINGS))
    fundraising = forms.ChoiceField(widget=forms.RadioSelect(choices=RATINGS))
    corporate_dev = forms.ChoiceField(label='Corporate Development', widget=forms.RadioSelect(choices=RATINGS))
