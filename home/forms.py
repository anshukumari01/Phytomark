from django import forms
from .models import Contact

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'subject', 'message']

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['placeholder'] = 'Enter Your Name'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter Your Email'
        self.fields['subject'].widget.attrs['placeholder'] = 'Enter Subject'
        self.fields['message'].widget.attrs['placeholder'] = 'Enter Your Message'
                                            
    