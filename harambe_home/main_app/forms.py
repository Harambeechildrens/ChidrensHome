from django import forms
from .models import Child, Staff, Donor
from datetime import datetime

class ChildRegistrationForm(forms.ModelForm):
    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        input_formats=["%Y-%m-%d"]
    )
    date_of_admission = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        input_formats=["%Y-%m-%d"]
    )

    class Meta:
        model = Child
        exclude = ['child_id'] 
        fields = '__all__'

class StaffRegistrationForm(forms.ModelForm):
    date_of_joining = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        input_formats=["%Y-%m-%d"]
    )

    class Meta:
        model = Staff
        exclude = ['staff_id'] 
        fields = '__all__'


class DonorForm(forms.ModelForm):
    class Meta:
        model = Donor
        fields = ['full_name', 'contact_info', 'donation_amount', 'donation_date', 'donation_type', 'notes']
        widgets = {
            'donation_date': forms.DateInput(attrs={'type': 'date'}),
        }
