from django.shortcuts import render, redirect
from .forms import signup_form, login_form
from django.contrib import messages
from django.contrib.auth import logout
from .models import userData
from django.db.models import F
def index(request):
    return render(request, "index.html")

def login(request):
    return render(request, "login.html")
def handle_signup(request):
    if request.method == 'POST':
        form = signup_form(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            referal = form.cleaned_data['referal']
            if(len(userData.objects.filter(email = email))>0):
                messages.error(request, 'Email already in use, please login')
                return redirect('/')
            if(len(referal) == 0):
                userData.objects.create(email = email, username = username, password=password, referral_code_used = referal)
            elif(len(referal) == 12):
                valid_referal = userData.objects.filter(referral_code_generated = referal)
                if(len(valid_referal)==1):
                    userData.objects.create(email = email, username = username, password=password, referral_code_used = referal)
                    user = userData.objects.get(referral_code_generated = referal)
                    user.number_of_referred = F('number_of_referred') + 1
                    user.save()
            else:
                messages.error(request, 'Invalid referal code')
                return redirect('/')
            return redirect("/login")
        else:
            messages.error(request, 'Invalid form data')
            return redirect('/')
    
def handle_login(request):
    if request.method == 'POST':
        form = login_form(request.POST)
        if(form.is_valid()):
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            if(len(userData.objects.filter(email=email, password = password))>0):
                query = userData.objects.filter(email=email).values('username', 'referral_code_generated', 'number_of_referred')
                context = {'username':query[0]['username'], 'referal_code':query[0]['referral_code_generated'], 'number_of_referred':query[0]['number_of_referred']}
                print(context)
                request.session['username'] = context['username']
                request.session['referal_code'] = context['referal_code']
                request.session['number_of_referred'] = context['number_of_referred']
                return redirect('/home')
            else:
                messages.error(request, 'Invalid login credentials')
                return redirect('/login')
        else:
            messages.error(request, 'Invalid form data')
            return redirect('/login')

def home(request):
    redirect('/home')
    print(len(request.session.items()))
    if(len(request.session.items())>0):
        users_reffered = userData.objects.filter(referral_code_used = request.session['referal_code']).values('username')
        context = {'username': request.session['username'], 'referal_code': request.session['referal_code'], 'number_of_referred':request.session['number_of_referred'], 'users_reffered':users_reffered}
        return render(request, "homepage.html", context)
    else:
        return redirect('/login')
def logout_view(request):
    request.session.flush()
    return redirect('/login')