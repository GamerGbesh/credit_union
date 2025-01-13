from django import forms
from datetime import date
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class MemberForm(forms.Form):
    COUNTRY_CODES = [("+233", "Ghana"),
                     ("+234", "Nigeria"),
                     ("+254", "Kenya"),
                     ("+256", "Uganda"),
                     ("+250", "Rwanda"),
                     ("+260", "Zambia"),
                     ("+263", "Zimbabwe"),
                     ("+27", "South Africa"),
                     ("+248", "Seychelles"),
                     ("+290", "Saint Helena"),
                     ("+291", "Eritrea"),
                     ("+297", "Aruba"),
                     ("+298", "Faroe Islands"),
                     ("+299", "Greenland"),
                     ("+228", "Togo")]
    
    first_name = forms.CharField(max_length=50, label="First name", required=True)
    last_name = forms.CharField(max_length=50, label="Last name", required=True)
    email = forms.EmailField(label="Email", required=False)
    code = forms.ChoiceField(choices=COUNTRY_CODES, label="Country code", required=True)
    msisdn = forms.RegexField(regex=r"^\d{9}$", required=True, label="Phone number")
    dob = forms.DateField(label="Date of birth", required=False, error_messages={"invalid": "Enter a valid date in MM/DD/YYYY format."})

    def clean(self):
        cleaned_data = super().clean()
        country_code = cleaned_data.get("code")
        msisdn = cleaned_data.get("msisdn")
        if country_code and msisdn:
            full_number = f"{country_code}{msisdn}"
            cleaned_data["full_number"] = full_number
        dob = cleaned_data.get("dob")
        
        if dob and dob > date.today():
            raise forms.ValidationError("Date of birth cannot be in the future.")
        first_name = cleaned_data.get("first_name")
        last_name = cleaned_data.get("last_name")
        first_name = first_name.split(" ")
        last_name = last_name.split(" ")
        if len(first_name) > 1 or len(last_name) > 1:
            raise forms.ValidationError("First and last name should be single words.")

        return cleaned_data
    

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "password1", "password2"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = user.username.lower()
        if commit:
            user.save()
        return user