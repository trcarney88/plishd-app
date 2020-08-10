import arrow
import stripe
import json
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from timeline.models import Accomplishment
from bragsheet_io import settings

stripe.api_key = settings.STRIPE_SK

def register(request, *args, **kwargs):
    if request.method == 'POST':
        plan = kwargs.get('plan')
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            try:
                form.save()
            except:
                pass
        
            if plan == 'Trial':
                return redirect('profile_create')
            else:
                return redirect('subscribe', plan=plan)
    else:
        form = UserRegisterForm()
        
    return render(request, 'users/register.html', context={'form': form})

@login_required
def profile_create(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            request.user.profile.subType = 'T'
            request.user.profile.endDate = arrow.now().shift(days=30).datetime
            form.save()
            request.user.profile.schedule_notification()
            print("Mobile No.: " + request.user.profile.mobileNumber)
            if request.user.profile.mobileNumber == '-1':
                request.user.profile.mobileNumber = ""
                request.user.profile.save()
                print("New Mobile No.: " + request.user.profile.mobileNumber)

            messages.success(request, f'Your Profile has been created! Your free trial will end on ' + arrow.get(request.user.profile.endDate).format('MMMM DD, YYYY'))
            return redirect('timeline', username=request.user.username)
        else:
            messages.error(request, f'The form is not valid.')
            print(form.errors)
    else:
        form = ProfileUpdateForm()

    return render(request, 'users/profile_create.html', context={'form':form})

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            request.user.profile.schedule_notification()
            messages.success(request, f'Your profile has been updated!')
            return redirect('profile_update')
        else:
            messages.error(request, f"Unable to update your profile.")
            return redirect('profile_update')

    u_form = UserUpdateForm(instance=request.user)
    p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
    }
    return render(request, 'users/profile_update.html', context=context)

@login_required
def account(request):
    if request.user.profile.subType == 'C' or request.user.profile.subType == 'T':
        daysLeft = (arrow.get(request.user.profile.endDate).date() - arrow.now().date()).days
    else:
        daysLeft = None
    if request.user.profile.subType == 'M' or request.user.profile.subType == 'Y':
        try:
            acctStatus = not stripe.Customer.retrieve(request.user.profile.stripe_cusId).delinquent
        except:
            acctStatus = "Unknown"
    else:
        acctStatus = None
    

    return render(request, 'users/profile.html', context={'daysLeft': daysLeft, 'acctStatus': acctStatus})

@login_required
def delete_account(request, *args, **kwargs):
    # Get the user object of the current user
    u = User.objects.get(username=kwargs.get('username'))
    # If the user is subscribed, cancel their subscription and prorate their account
    if request.user.profile.subType == 'M' or request.user.profile.subType =='Y':
        sub = request.user.profile.stripe_subId
        cus = request.user.profile.stripe_cusId
        stripe.Subscription.delete(sub)
        stripe.Customer.delete(cus)

    # Delete all the accomplishment associated with the user
    accomps = Accomplishment.objects.filter(user=u)
    for a in accomps:
        a.delete()

    # Make user inactive
    logout(request)
    u.delete()
    
    return render(request, 'users/profile_delete.html')

@login_required
def subscribe(request, *args, **kwargs):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            request.user.profile.schedule_notification()
            if request.POST.get('pricing') == 'yearly':
                plan = 'Yearly'
                monthly = None
                yearly = 'checked'
            else:
                plan = 'Monthly'
                monthly = 'checked'
                yearly = None

            status, errorMsg = startSubscription(request) # Need to create customer and subscription
            if status:
                messages.success(request, f"Your payment succeeded. Thank you for subscribing.")
                return redirect('timeline', username=request.user.username)
            else:
                messages.error(request, f"Unable to process subscription. " + errorMsg)
                return redirect('subscribe')
            
    else:
        plan = kwargs.get('plan')
        if plan == 'Trial':
            return redirect('profile_create')
        elif plan == 'Yearly':
            monthly = None
            yearly = 'checked'
        else:
            monthly = 'checked'
            yearly = None

        form = ProfileUpdateForm()

    return render(request, 'users/subscribe.html', context={'form':form, 'pubKey': settings.STRIPE_PK, 'plan': plan, 'monthly': monthly, 'yearly': yearly, 'btnText': "Subscribe"})

@login_required
def cancelSub(request, *args, **kwargs):
    u = User.objects.get(username=kwargs.get('username'))
    if u.profile.subType == 'M' or u.profile.subType == 'Y':
        try:
            stripe.api_key(settings.STRIPE_SK)
            sub = stripe.Subscription.modify(u.profiles.stripe_subId, cancel_at_period_end=True)
            endDate = arrow.get(sub.current_period_end)
            u.profile.subType = 'C'
            u.profile.endDate = endDate.datetime

            messages.success(request, 'Your subscription has been successfully cancelled. You will have access until ' + endDate)
        except Exception as e:
            messages.error(request, 'Your subscription could not be canceled. ' + str(e) + '. Please send us an email to have your subscription cancelled.')
    else:
        if (u.profile.subType == 'T' and (arrow.get(u.profile.endDate).date() - arrow.now().date()).days <= 30) or u.profile.subType == 'C':
            messages.warning(request, "You don't have a subscription. You have access until " + str(u.profile.endDate))
        else:
            messages.warning(request, "Why are you trying to cancel? Your subscription is free.")

    return redirect('profile')

@login_required
def payment(request, *args, **kwargs):
    if request.method == 'POST':
        pricing = request.POST.get('pricing')
        print("Current Customer ID: " + request.user.profile.stripe_cusId)
        print("Current Subscription ID: " + request.user.profile.stripe_subId)
        if request.user.profile.stripe_cusId == "None":
            print("User has no customer ID")
            status, errorMsg = startSubscription(request) # Need to create customer and subscription
            if status:
                messages.success(request, f"Your payment succeeded. Thank you for subscribing.")
        elif request.user.profile.stripe_subId == "None":
            print("User has no subscription ID")
            status, errorMsg = createSubscription(request) # Customer needs to create a subscription
            if status:
                messages.success(request, f"Your payment succeeded. Thank you for subscribing.")
        else: # A Subscription already exists
            print("User currently has a subscription")
            # pricing and subType are the same, only need to modify payment method
            if pricing == 'monthly' and request.user.profile.subType == 'M':
                print("User has a monthly plan an is updating payment information.")
                status, errorMsg = modifyCustomer(request)
                if status:
                    messages.success(request, f"Your payment infomation has been updated.")
            elif pricing =='yearly' and request.user.profile.subType == 'Y':
                print("User has a yearly plan an is updating payment information.")
                status, errorMsg = modifyCustomer(request)
                if status:
                    messages.success(request, f"Your payment infomation has been updated.")
            # pricing and subType are not equal, need to modify payment method and subscription
            else:
                currPlan = 'monthly' if request.user.profile.subType == 'M' else 'yearly'

                print("User is changing from a " + currPlan + " to " + pricing)
                status, errorMsg = modifyCustomer(request)
                if status:
                    status, errorMsg, billDate = modifySubscription(request)
                    if status:
                        messages.success(request, f"Your payment succeeded and your subscription has been changed. You will be charged the new amount on " + arrow.get(billDate).format('MMMM DD, YYYY'))
        if not status:
            messages.error(request, f'Your payment failed. ' + errorMsg)
            return redirect('payment', plan=pricing)
        else:
            return redirect('profile')
    else:
        plan = kwargs.get('plan')
        if plan == 'Yearly':
            monthly = None
            yearly = 'checked'
        else:
            monthly = 'checked'
            yearly = None

        return render(request, 'users/payment.html', context={'pubKey': settings.STRIPE_PK, 'plan': plan, 'monthly': monthly, 'yearly': yearly, 'btnText': "Pay"})

def startSubscription(request):
    status, errMsg = modifyCustomer(request)
    if status:
        status, errMsg = createSubscription(request)
    return (status, errMsg)

def createSubscription(request):
    if request.method == 'POST':
        pricing = request.POST.get('pricing')
        print("Pricing: " + pricing)

        if not request.user.profile.usedTrial:
            trialEnd = arrow.get(request.user.profile.endDate).timestamp
        else:
            trialEnd = None

        if  pricing == 'monthly':
            plan = settings.MONTHLY_PLAN_ID
            request.user.profile.subType = 'M'
        elif pricing == 'yearly':
            plan = settings.YEARLY_PLAN_ID
            trialEnd = None
            request.user.profile.subType = 'Y'
        try:    
            sub = stripe.Subscription.create(
                customer = request.user.profile.stripe_cusId,
                items = [
                    {
                        "plan": plan,
                    },
                ],
                trial_end = trialEnd,
                expand = ["latest_invoice.payment_intent"]
            )
            print("Subscription ID: " + sub.id)
            request.user.profile.stripe_subId = sub.id
            request.user.profile.usedTrial = True
            request.user.profile.save()
            return (True, "")
        except Exception as e:
            return (False, str(e))

def modifySubscription(request):
    # To modify the subscription, we save the current subscriptions period end date, delete the current subscription, 
    # then create a new subscription with the new plan and a free trial to the save period end date. The customer 
    # won't be charged until the trial date is reached.
    if request.method == 'POST':
        pricing = request.POST.get('pricing')

        if  pricing == 'monthly':
            plan = settings.MONTHLY_PLAN_ID
            request.user.profile.subType = 'M'
        elif pricing == 'yearly':
            plan = settings.YEARLY_PLAN_ID
            request.user.profile.subType = 'Y'

        try:
            sub = stripe.Subscription.retrieve(request.user.profile.stripe_subId)
            trial = sub.current_period_end
            stripe.Subscription.delete(request.user.profile.stripe_subId)
            sub = stripe.Subscription.create(
                customer=request.user.profile.stripe_cusId,
                items = [
                    {
                        "plan": plan,
                    },
                ],
                trial_end = trial,
                expand = ["latest_invoice.payment_intent"]
            )

            request.user.profile.stripe_subId = sub.id
            request.user.profile.save()

            return [True, "", trial]
        except Exception as e:
            return [False, str(e), ""]

def modifyCustomer(request):
    if request.method == 'POST':
        print("Payment Method: " + request.POST.get('payment_method'))
        pm = request.POST.get('payment_method')

        if request.user.profile.stripe_cusId == "None":
            try:
                customer = stripe.Customer.create(
                    payment_method = pm,
                    email = request.user.email,
                    invoice_settings = {'default_payment_method': pm},
                    name = request.POST.get('firstName') + " " + request.POST.get('lastName'),
                    address={
                        'line1': request.POST.get('addrLine1'),
                        'line2': request.POST.get('addrLine2'),
                        'city': request.POST.get('addrCity'),
                        'state': request.POST.get('addrState'),
                        'postal_code': request.POST.get('addrZip')
                    }
                )
                print("Customer ID: " + customer.id)
                request.user.profile.stripe_cusId = customer.id
                request.user.profile.save()
                return (True, "")
            except Exception as e:
                return (False, str(e))
        else:
            try:
                stripe.PaymentMethod.attach(
                    pm,
                    customer=request.user.profile.stripe_cusId
                )
                stripe.Customer.modify(
                    request.user.profile.stripe_cusId,
                    invoice_settings={'default_payment_method': pm}
                )
                return (True, "")
            except Exception as e:
                return (False, str(e))