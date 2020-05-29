from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login as lo
from accounts.models import User
from home.views import dashboard
from django.contrib import messages
from django.conf import settings
from django.utils.http import is_safe_url
from django.urls import reverse
from django.contrib.auth import logout 
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes,force_text,DjangoUnicodeDecodeError
from .utils import generate_token
from django.core.mail import EmailMessage


# Create your views here.

def login(request):
    if request.method == "POST":
        a = request.POST["username"]
        b = request.POST["pass"]
        user = authenticate(request , username = a, password = b)
        next_ = request.GET.get('next',settings.LOGIN_REDIRECT_URL)
        next_post = request.POST.get('next')
        redirect_path = next_ or next_post or None
        print(user)
        if user is not None:
            lo(request, user)
            return HttpResponseRedirect(request.GET.get('next',settings.LOGIN_REDIRECT_URL))
            
        elif User.obb.filter( username = a ).exists():
            messages.info(request,'Passward not matched')
            return redirect('/')
        
        else:
            messages.info(request,'Username and Passward not matched')
            return redirect('/')
        
    else:
        return render(request,'index.html')



def register(request):
    if request.method == 'POST':
        pid = request.POST["username"]
        uMail = request.POST["email"]
        # uNumber = request.POST["p_number"]
        pswd = request.POST["pass"]
        pswd1 = request.POST["pass1"]

        if User.obb.fillter(username = pid).exists():
            messages.info(request,'account is already exist')
        elif pswd == pswd1:
            user = User.obb.create_user(username = pid, email = uMail, password = pswd1 )
            if user is not None:
                user.save()

                current_site=get_current_site(request)
                email_subject='Activate your Account',
                message=render_to_string('/activate.html',
                {
                    'user':user,
                    'domain':current_site.domain,
                    'uid':urlsafe_base64_encode(force_bytes( user.pk))
                    'token':generate_token.make_token(user)
                }
                )
                email_message = EmailMessage(
                email_subject,
                message,
                settings.EMAIL_HOST_USER,
                ['to1@example.com', 'to2@example.com'],
                )

                email_message.send()
 

                messages.info(request,'Now you can login')
                return redirect('/')
            else:
                messages.info(request,'Please enter details')
                return redirect('register')
        else:
            return redirect('register')
    else:
        return render(request,'reg.html')

def validate_username(request):
    username = request.GET.get('username', None)
    data = {
        'is_taken': User.obb.filter(username=username).exists()
    }
    return JsonResponse(data)

def out_view(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("/")

class ActivateAccountView(View):
    def get(self,request,uidb64,token):
        try:
            uid=force_text(urlsafe_base64_decode(uidb64))
            user=user.objects.get(pk=uid)
        except Exception as identifier:
            user=None

        if user is not None and generate_token.check_token(user,token):
            user.is_active=True
            user.save()
            messages.add_message(request,messages.INFO,'account activated successfully')
            return redirect('login')

        return render(request,'/activate_failed.html',status=401)