from django import forms
from .models import LostItem, FoundItem


class LostItemForm(forms.ModelForm):
    class Meta:
        model = LostItem
        fields = ['title', 'category', 'description', 'location', 'date_lost', 'image', 'reward', 'contact_info']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. Blue Backpack'}),
            'category': forms.Select(attrs={'class': 'form-input'}),
            'description': forms.Textarea(attrs={'class': 'form-input', 'rows': 4,
                                                   'placeholder': 'Describe the item in detail...'}),
            'location': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. Library, 2nd Floor'}),
            'date_lost': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-input-file'}),
            'reward': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Optional, e.g. ₹200'}),
            'contact_info': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Phone or email'}),
        }


class FoundItemForm(forms.ModelForm):
    class Meta:
        model = FoundItem
        fields = ['title', 'category', 'description', 'location', 'date_found', 'image', 'contact_info']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. Silver Wristwatch'}),
            'category': forms.Select(attrs={'class': 'form-input'}),
            'description': forms.Textarea(attrs={'class': 'form-input', 'rows': 4,
                                                   'placeholder': 'Describe the item in detail...'}),
            'location': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. Canteen'}),
            'date_found': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-input-file'}),
            'contact_info': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Phone or email'}),
        }
