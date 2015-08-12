from django import forms
from django.core.validators import RegexValidator
from main.models import City

letter_validator = RegexValidator(r'^[a-zA-Z]*$', 'Please Type Letters')

class CitySearch(forms.Form):
	name = forms.CharField(required=True, validators=[letter_validator])

class CreateCity(forms.ModelForm):
	class Meta:
		model = City
		fields = '__all__'

class UserSignUp(forms.Form):
	name = forms.CharField(required=True, validators=[letter_validator])
	email = forms.CharField(required=True)
	password = forms.CharField(widget=forms.PasswordInput(), required=True)