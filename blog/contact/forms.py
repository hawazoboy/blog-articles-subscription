from django import forms

class ContactUsForm(forms.Form):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'class' : 'form-control',
        'placeholder' : 'your name'
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class' : 'form-control',
        'placeholder' : 'your email'
    }))
    subject = forms.CharField(max_length=200, widget=forms.TextInput(attrs={
        'class' : 'form-control',
        'placeholder' : 'your subject'
    }))
    message = forms.CharField(widget=forms.Textarea(attrs={
        'class' : 'form-control',
        'placeholder' : 'your message'
    }))
    