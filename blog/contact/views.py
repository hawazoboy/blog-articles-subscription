from django.shortcuts import render
from .forms import ContactUsForm
from .models import ContactUs

def Contact_Us(request):
    if request.method == 'POST':
        form = ContactUsForm(request.POST)
        if form.is_valid():
            ContactUs.objects.create(
                name=form.cleaned_data.get('name'),
                email=form.cleaned_data.get('email'),
                subject=form.cleaned_data.get('subject'),
                message=form.cleaned_data.get('message'))
    
    else:
        form = ContactUsForm()

    return render(request, 'contact.html', {'form':form})