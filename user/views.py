from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.http import HttpResponseRedirect, HttpResponse
from django.template import loader
from django.db import transaction
from .models import Profile, Fill_Out_Sheet, Message
from .forms import UserForm, ProfileUpdateForm, FillOutSheetForm, MessageForm, ChatForm, ActiveTutorForm
from django.contrib import messages
from django.conf import settings
import stripe
from django.core.paginator import Paginator

# Create your views here

# https://www.youtube.com/watch?v=CQ90L5jfldw&list=PL-osiE80TeTtoQCKZ03TU5fNfx2UY6U4p&index=9: tutorial used to create Profile update
# https://medium.com/@jainsahil1997/simple-google-authentication-in-django-58101a34736b: tutorial to create login
# https://testdriven.io/blog/django-stripe-tutorial/: tutorial for setting up stripe

stripe.api_key = settings.STRIPE_SECRET_KEY


@login_required
def Home(request):
    available_tutors = Profile.objects.filter(active_tutor=True)
    template = loader.get_template('home.html')

    count = 0
    msgs = Message.objects.filter(receiver=request.user)
    for msg in msgs:
        if (msg.read == False):
            count += 1

    context = {
        "count":count,
    }
    return render(request, 'home.html', context)


@login_required
def filloutform(request, tutor_username):
    count = 0
    msgs = Message.objects.filter(receiver=request.user)
    for msg in msgs:
        if (msg.read == False):
            count += 1
    try:
        receiver_ob = User.objects.get(username=tutor_username)
    except User.DoesNotExist:
        return render(request, '404.html')
    if request.method == 'POST':
        try:
            form = FillOutSheetForm(request.POST, instance=request.user)
        except Fill_Out_Sheet.DoesNotExist:
            return render(request, '404.html')
        if form.is_valid():
            try:
                receiver_ob = User.objects.get(username=tutor_username)
            except User.DoesNotExist:
                return render(request, '404.html')
            formContent = Fill_Out_Sheet(
                has_tutor_accepted=False,
                has_tutor_rejected=False,
                no_response=True,
                sender=request.user,
                receiver=receiver_ob,
                class_desc=form.cleaned_data['class_desc'],
                help_desc=form.cleaned_data['help_desc'],
                time_slot=form.cleaned_data['time_slot'],
                meeting_places=form.cleaned_data['meeting_places']
            )
            formContent.save()
            return HttpResponseRedirect("/confirm")
    else:
        form = FillOutSheetForm()

    context = {'form': form, 'receiver_ob': receiver_ob, "count": count,}
    return render(request, 'filloutsheet.html', context)


@login_required
def DeleteSheet(request, form_id):
    try:
        sheet = Fill_Out_Sheet.objects.get(id = form_id)
    except Fill_Out_Sheet.DoesNotExist:
        return render(request, '404.html')
    if request.method == "GET":
        sheet.delete()
    context = {
        "sheet":sheet
    }
    return redirect("/requestsUpdate")

@login_required
def RequestsUpdate(request):
    count = 0
    msgs = Message.objects.filter(receiver=request.user)
    for msg in msgs:
        if (msg.read == False):
            count += 1

    key = settings.STRIPE_PUBLISHABLE_KEY
    awaiting = Fill_Out_Sheet.objects.filter(sender = request.user).filter(no_response = True)
    accepted = Fill_Out_Sheet.objects.filter(sender = request.user).filter(no_response = False).filter(has_tutor_accepted=True)
    rejected = Fill_Out_Sheet.objects.filter(sender = request.user).filter(no_response = False).filter(has_tutor_rejected=True)
    template = loader.get_template('requestUpdates.html')

    context = {
        'count': count,
        'awaiting':awaiting,
        'accepted':accepted,
        'rejected':rejected,
        'key':key,
    }

    return render(request, 'requestUpdates.html', context)

@login_required
def confirm(request):
    count = 0
    msgs = Message.objects.filter(receiver=request.user)
    for msg in msgs:
        if (msg.read == False):
            count += 1
    context = {
        "count": count,
    }
    return render(request, 'confirm.html', context)

@login_required
def confirm_Accept(request):
    count = 0
    msgs = Message.objects.filter(receiver=request.user)
    for msg in msgs:
        if (msg.read == False):
            count += 1
    context = {
        "count": count,
    }
    return render(request, '/confirm_Accept', context)

@login_required
def confirm_Reject(request):
    count = 0
    msgs = Message.objects.filter(receiver=request.user)
    for msg in msgs:
        if (msg.read == False):
            count += 1
    context = {
        "count": count,
    }
    return render(request, '/confirm_Reject', context)

@login_required
def GetHelp(request):
    count = 0
    msgs = Message.objects.filter(receiver=request.user)
    for msg in msgs:
        if (msg.read == False):
            count += 1

    key = settings.STRIPE_PUBLISHABLE_KEY
    awaiting = Fill_Out_Sheet.objects.filter(sender = request.user).filter(no_response = True)
    accepted = Fill_Out_Sheet.objects.filter(sender = request.user).filter(no_response = False).filter(has_tutor_accepted=True)
    rejected = Fill_Out_Sheet.objects.filter(sender = request.user).filter(no_response = False).filter(has_tutor_rejected=True)
    available_tutors = Profile.objects.filter(active_tutor=True)
    template = loader.get_template('gethelp.html')
    
    classes_taken_query = request.GET.get('classes_taken')
    year_query = request.GET.get('year')

    if classes_taken_query != '' and classes_taken_query is not None:
        available_tutors = available_tutors.filter(classes_taken__icontains=classes_taken_query)
    
    if year_query != '' and year_query is not None:
        available_tutors = available_tutors.filter(year__icontains=year_query)

    context = {
        'available_tutors': available_tutors,
        'awaiting':awaiting,
        'accepted':accepted,
        'rejected':rejected,
        'key':key,
        'count':count,
    }

    return render(request, 'gethelp.html', context)

@login_required
def charge(request):
    count = 0
    msgs = Message.objects.filter(receiver=request.user)
    for msg in msgs:
        if (msg.read == False):
            count += 1
    
    context = {
        "count": count,
    }

    if request.method == 'POST':
        charge = stripe.Charge.create(
            amount=2000,
            currency='usd',
            description='A Django Charge',
            source=request.POST['stripeToken']
        )
        return render(request, 'charge.html', context)
    
    return render(request, 'charge.html', context)


@login_required
def Messaging(request):

    count = 0
    msgs = Message.objects.filter(receiver=request.user)
    for msg in msgs:
        if (msg.read == False):
            count += 1

#   Makes the list of people who you've messaged or who have messaged you
    received = Message.objects.filter(receiver=request.user)
    sent = Message.objects.filter(sender=request.user)
    pen_pals = []
    pen_pals_unread = []

    for msg in received:
        if not msg.read:
            if msg.sender not in pen_pals_unread:
                pen_pals_unread.append(msg.sender)
    
    for msg in received:
        if msg.sender not in pen_pals:
            pen_pals.append(msg.sender)
    for msg in sent:
        if msg.receiver not in pen_pals:
            pen_pals.append(msg.receiver)

    paginator = Paginator(pen_pals, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj":page_obj,
        "count":count,
        "pen_pals_unread":pen_pals_unread,
    }
    return render(request, 'send.html', context)

@login_required
def CorLog(request, pal_username):
    

    try:
        pen_pal = User.objects.get(username=pal_username)
    except User.DoesNotExist:
        return render(request, '404.html')
    coris = []
    # Make send box at bottom of screen
    if request.method == "POST":

        try:
            form = ChatForm(request.POST, instance=request.user)
        except ChatForm.DoesNotExist:
            return render(request, '404.html')
       
        if form.is_valid():
            msg = Message(
                sender = request.user,
                receiver = pen_pal,
                msg_content = form.cleaned_data['msg_content'],
            )
            msg.save()

    form = ChatForm()

    allMsg = Message.objects.filter(receiver=pen_pal, sender=request.user) | Message.objects.filter(receiver=request.user, sender=pen_pal)
    allMsgOrdered = allMsg.order_by('-created_at')
    for i in allMsgOrdered:
        coris.append(i)
    
    coris.sort(key=(lambda x: x.created_at), reverse=True)

    received_messages = Message.objects.filter(receiver = request.user, sender = pen_pal)

    for message in received_messages:
        message.read = True
        message.save()

    count = 0
    msgs = Message.objects.filter(receiver=request.user)
    for msg in msgs:
        if (msg.read == False):
            count += 1

    context = {
        'coris': coris,
        'pal' : pen_pal,
        'form' : form,
        'count':count,
    }
    return render(request, 'log.html', context)

@login_required
def SeeProfile(request):
    count = 0
    msgs = Message.objects.filter(receiver=request.user)
    for msg in msgs:
        if (msg.read == False):
            count += 1
    
    context = {
        "count":count,
    }
    return render(request, 'profile.html', context)

@login_required
def GiveHelp(request):
    count = 0
    msgs = Message.objects.filter(receiver=request.user)
    for msg in msgs:
        if (msg.read == False):
            count += 1
    
    if request.method == 'POST':
        try:
            at_form = ActiveTutorForm(request.POST, request.FILES, instance=request.user.profile)
        except ActiveTutorForm.DoesNotExist: 
            return render(request, '404.html')
        
        if at_form.is_valid():
            at_form.save()
            return redirect('givehelp.html')
    else:
        try:
            at_form = ActiveTutorForm(instance=request.user)
        except ActiveTutorForm.DoesNotExist: 
            return render(request, '404.html')
        
    tut = request.user.profile

    received = Fill_Out_Sheet.objects.filter(receiver=request.user).filter(no_response = True)
    context = {'received':received,'at_form': at_form, 'tut':tut, "count":count,}
    return render(request, 'givehelp.html', context)

@login_required
def AcceptTutee(request, form_id):
    count = 0
    msgs = Message.objects.filter(receiver=request.user)
    for msg in msgs:
        if (msg.read == False):
            count += 1

    try:
        sheet = Fill_Out_Sheet.objects.get(pk = form_id)
    except Fill_Out_Sheet.DoesNotExist:
        return render(request, '404.html')
    sheet.no_response = False
    sheet.has_tutor_accepted = True
    sheet.has_tutor_rejected = False
    sheet.save()
    context = {'sheet':sheet,"count":count,}
    return render(request, 'confirm_Accept.html', context)

@login_required
def RejectTutee(request, form_id):
    count = 0
    msgs = Message.objects.filter(receiver=request.user)
    for msg in msgs:
        if (msg.read == False):
            count += 1
    try:
        sheet = Fill_Out_Sheet.objects.get(pk = form_id)
    except Fill_Out_Sheet.DoesNotExist:
        return render(request, '404.html')
    sheet.delete()
    context = {'sheet':sheet,"count":count,}
    return render(request, 'confirm_Reject.html', context)

@login_required
def Prof(request):
    count = 0
    msgs = Message.objects.filter(receiver=request.user)
    for msg in msgs:
        if (msg.read == False):
            count += 1
    
    if request.method == 'POST':
        try:
            u_form = UserForm(request.POST, instance=request.user)
        except UserForm.DoesNotExist:
            return render(request, '404.html')
       
        try:
             p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        except ProfileUpdateForm.DoesNotExist:
            return render(request, '404.html')
       
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('update_profile.html')
    else:
        try:
            u_form = UserForm(instance=request.user)
        except UserForm.DoesNotExist:
            return render(request, '404.html')
       
        try:
            p_form = ProfileUpdateForm(instance=request.user.profile)
        except ProfileUpdateForm.DoesNotExist:
            return render(request, '404.html')

    context = {
        'u_form': u_form,
        'p_form': p_form, 
        "count":count,
    }
    return render(request, 'update_profile.html', context)

def Logout(request):
    logout(request)
    return HttpResponseRedirect('/')
