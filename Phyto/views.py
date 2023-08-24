from django.shortcuts import render,HttpResponse, redirect
from home.models import Banner
from home.models import Placeholder
from home.models import About
from home.models import Fproduct
from home.models import Info
from home.models import Service
from home.models import OrganicFarming
from about.models import Carousel
from about.models import Aboutus
from about.models import Seperation
from django.core.mail import send_mail
from django.contrib import messages
from home.forms import ContactForm


# Create your views here.
def home(request):
    banner = Banner.objects.first()
    placeholders = Placeholder.objects.all().order_by('-id')[:2]
    about = About.objects.first()
    fproduct = Fproduct.objects.all()
    info = Info.objects.first()

    context={
        'banner':banner,
        'placeholder': placeholders,
        'about': about,
        'fproduct': fproduct,
        'info': info
    }
    return render(request, 'index.html', context)

def about(request):
    info = Info.objects.first()
    about = About.objects.first()
    carousel = Carousel.objects.all().order_by('-id')[:3]
    aboutus = Aboutus.objects.first()
    seperation = Seperation.objects.first()
    context={
        'info': info,
        'about': about,
        'carousel': carousel,
        'aboutus': aboutus,
        'seperation': seperation
    }
    return render(request, 'about.html', context)


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            email = form.cleaned_data["email"]
            subject = form.cleaned_data["subject"]
            message = form.cleaned_data["message"]
            form.save()

            # Send the email
            send_mail(
                subject,
                f"Name: {name}\nEmail: {email}\n\n{message}",
                email,
                ['phytomark6@gmail.com'],  
                fail_silently=False,
            )
            messages.success(request, 'Thanks for contacting us! Your message has beed received ')

            return redirect('contact')  # Redirect to a success page
    else:
        form = ContactForm()

    
    info = Info.objects.first()
    about = About.objects.first()

    context={
        'info': info,
        'about': about,
        'form': form
    }
    return render(request, 'contact.html', context)


def services(request):
    info = Info.objects.first()
    about = About.objects.first()
    service = Service.objects.all().order_by('id')
    context={
        'info': info,
        'about': about,
        'service' : service
    }
    return render(request, 'services.html', context)


def farming(request):
    info = Info.objects.first()
    about = About.objects.first()
    farming = OrganicFarming.objects.first()
    context={
        'info': info,
        'about': about,
        'farming' : farming
    }
    return render(request, 'farming.html', context)
