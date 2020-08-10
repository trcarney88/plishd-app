from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Field, Row
from crispy_forms.bootstrap import PrependedText
from .models import Accomplishment

class DateInput(forms.DateInput):
    input_type = 'date'

class NewAccomplishmentForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea(attrs={'placeholder':'It is recommended you not include proprietary, or company sensitive information in your accomplishments.'}))
    date = forms.DateField(widget=DateInput)
    
    class Meta:
        model = Accomplishment
        labels = {'date':'Date', 'jobTitle':'Job Title', 'company':'Company', 'text':'Accomplishment'}
        fields = ['date', 'jobTitle', 'company', 'text']