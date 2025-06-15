from django import forms
from .models import Nurse, NurseDocument, Shift, Booking

class NurseForm(forms.ModelForm):
    class Meta:
        model = Nurse
        fields = ['full_name', 'dob', 'registration_number', 'specialty']
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date'}),
        }

class NurseDocumentForm(forms.ModelForm):
    class Meta:
        model = NurseDocument
        fields = ['document_type', 'file_url', 'expiry_date']
        widgets = {
            'expiry_date': forms.DateInput(attrs={'type': 'date'}),
        }

class ShiftForm(forms.ModelForm):
    class Meta:
        model = Shift
        fields = ['ward', 'specialty_required', 'po_number', 'shift_date', 'shift_time']
        widgets = {
            'shift_date': forms.DateInput(attrs={'type': 'date'}),
            'shift_time': forms.TimeInput(attrs={'type': 'time'}),
        }

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['nurse'] 