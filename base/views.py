import arrow
import stripe
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.core.mail import send_mail, BadHeaderError
from django.contrib import messages
from .forms import ContactForm
from bragsheet_io import settings
from users.forms import ProfileUpdateForm
from timeline.models import Accomplishment
from django.contrib.auth.models import User

# Create your views here.
def home(request):
    # No one is logged in
    if request.user.username == '':
        return render(request, 'base/home.html')
    # Logged in User is using the free trial or I have given them free access
    elif request.user.profile.subType == 'T':
        today = arrow.now().date()
        endDate = arrow.get(request.user.profile.endDate).date()
        # Free trial is over
        if today > endDate:
            request.user.profile.usedTrial = True
            request.user.profile.save()
            messages.error(request, f'Your free trial has ended. Please Subscribe now')
            return redirect('payments')
        # Free trial is still active
        elif (endDate - today).days <= 30:
            diff = endDate - today
            messages.warning(request, "You have " + str(diff.days) + " left in your Free Trial. Go to your profile to Subscribe NOW!")
            return redirect('timeline', username=request.user.username)
        # The lucky fuck with free access
        else:
            messages.success(request, f'Your subscription is free you lucky fuck.')
            return redirect('timeline', username=request.user.username)
    # User is subscriped, Check to make sure they are not delinquent on payments
    elif request.user.profile.subType == 'M' or request.user.profile.subType == 'Y':
        if stripe.Customer.retrieve(request.user.profile.stripe_cusId).delinquent:
            messages.error(request, f'Your last payment did not go through. Please update your payment information now.')
            return redirect('payments')
        else:
            return redirect('timeline', username=request.user.username)
    # User has cancelled their subscription, they get until the end of the month or year depending on the subscription
    elif request.user.profile.subType == 'C':
        today = arrow.now().date()
        endDate = arrow.get(request.user.profile.endDate).date()
        if today > endDate:
            messages.error(request, f'Your subscription has been cancelled. Please let us know what we can do to get you back.')
            return redirect('contact')
        else:
            diff = endDate - today
            messages.warning(request, "You have " + str(diff.date()) + " left until your subscription is cancelled. Go to your profile to Resubscribe NOW!")
            return redirect('timeline', username=request.user.username)
    else:
        return render(request, 'base/home.html')

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)

        if form.is_valid():
            subject = "From Contact Form"
            from_email = settings.CONTACT_EMAIL
            message = "From: " + form.cleaned_data['email'] + "\n\nSubject: " + form.cleaned_data['subject'] + "\n\nMessage:\n" + form.cleaned_data['message']
            try:
                send_mail(subject, message, from_email, [settings.CONTACT_EMAIL])
            except BadHeaderError:
                messages.error(request, 'Invalid header found.')
                return render(request, 'base/contact.html', {'form': form})

            messages.success(request, 'Thank you for reaching out to us, We will get back to you shortly.')
            return redirect('contact')

    else:
        form = ContactForm()

    return render(request, "base/contact.html", {'form': form})

def about(request):
    user_count = len(User.objects.filter(is_active=True))
    accomp_count = len(Accomplishment.objects.filter())
    return render(request, 'base/about.html', {'user_count': user_count, 'accomp_count': accomp_count})

def cookies(request):
    return render(request, 'base/cookies.html')
    
