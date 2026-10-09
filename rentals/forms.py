from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text='Required. Please provide a valid email.')

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email',)


class AvailabilityForm(forms.Form):
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    capacity = forms.IntegerField(min_value=1, label="Number of Seats")

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")

        if start_date and end_date and end_date <= start_date:
            raise forms.ValidationError("End date must be after the start date.")
        return cleaned_data


class BookingConfirmationForm(forms.Form):
    full_name = forms.CharField(max_length=100, required=True)
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=True)
    license_number = forms.CharField(max_length=50, required=True)
    agree_to_terms = forms.BooleanField(
        required=True,
        label="I have read and agree to the terms and conditions of the rental agreement.",
    )
