from django.contrib.auth import authenticate, logout, get_user_model, update_session_auth_hash, login
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from .tokens import account_activation_token
from .forms import LoginForm, RegisterForm, PasswordForm, ResetPasswordForm, AccountForm
from django.contrib import messages
from django.core.mail import EmailMessage
from .models import Account


@login_required
def index(request):
    return render(request, 'profile.html')


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            username = cd['username']
            password = cd['password']
            user = authenticate(username=username, password=password)
            login(request, user)
            if user and user is not None:
                messages.success(request=request, message=str(user) + " عزیز خوش آمدید ")
                return render(request, 'restaurant.html', {'form': form})
            else:
                messages.error(request=request, message='متاسفانه کاربری با این مشخصات موجود نیست')
                return render(request, 'login.html', {'form': form})
        return render(request, 'login.html', {'form': form})
    else:
        form = LoginForm()
        return render(request, 'login.html', {"form": form})


def activateEmail(request, user, param):
    mail_subject = 'فعالسازی حساب کاربری'
    message = render_to_string('activate_account.html', {
        'user': user,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[param])
    if email.send():
        messages.success(request, f'{user} گرامی از اینکه به خانواده رستوران آبی می پیوندید بسیار خرسندیم'
                                  f' لطفا به پست الکرونیکی خود {param} مراجعه کرده بر روی لینک فعالسازی کلیک کنید')
    else:
        messages.error(request, f'متاسفانه قادر به ارسال ایمیل به آدرس {param}'
                                f'نیستیم لطفا مجددا آدرس پست الکترونیک خود را چک کنید')


def activate(request, uid64, token):
    user_model = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uid64))
        user = user_model.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, user_model.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'با سپاس فراوان پست الکترونیک شما تایید و حساب کاربری شما فعال شد')
        return redirect('login')
    else:
        messages.error(request, 'متاسفیم لینک وارد شده صحیح نمیباشد یا زمان آن منقضی شده است')
        return redirect('register')


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            username = cd['username']
            password1 = cd['password1']
            email = cd['email']
            first_name = cd['first_name']
            last_name = cd['last_name']
            user = User.objects.create_user(username=username, password=password1, email=email)
            user.first_name = first_name
            user.last_name = last_name
            user.is_active = False
            user.save()
            activateEmail(request, user, cd['email'])
            return redirect('profile')
        return render(request, 'register.html', {'form': form})
    else:
        form = RegisterForm()
        return render(request, 'register.html', {"form": form})


@login_required
def profile_view(request):
    if request.method == 'POST':
        form = AccountForm(request.POST)
        avatar = request.FILES['avatar']
        logo = request.FILES['logo']
        if form.is_valid():
            cd = form.cleaned_data
            company = cd['company']
            tel = cd['tel']
            cat = cd['cat']
            address = cd['address']
            acc = Account.objects.create(user=request.user, logo=logo, avatar=avatar, tel=tel, address=address,
                                         company=company, cat=cat)
            acc.save()
            if acc and acc is not None:
                messages.success(request, 'حساب کاربری شما تغییر یافت')
            else:
                messages.error(request, 'متاسفیم خطایی رخ داد لطفا مجددا تلاش کنید')
            return redirect('res_admin')
        else:
            messages.error(request, 'form is not valid ' + str(form.cleaned_data) + " " + str(request.FILES))
            return redirect('profile')
    else:
        acc = Account.objects.filter(user=request.user).first()
        if acc and acc is not None:
            form = AccountForm(initial={'logo': acc.logo, 'avatar': acc.avatar, 'tel': acc.tel, 'address': acc.address,
                                        'company': acc.company, 'cat': acc.cat})
        else:
            form = AccountForm()
        return render(request, 'profile.html', {'form': form, 'acc': acc})


@login_required
def logout_view(request):
    user = request.user
    if user is not None and user.is_authenticated:
        logout(request)
        return redirect('login')
    else:
        messages.info(request=request, message='حساب کاربری شما در دست نیست لطفا ابتدا وارد حساب خود شوید')
        return redirect('logout')


def password_reset_view(request):
    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            email_to = form.cleaned_data['email']
            user = User.objects.filter(email=email_to).first()
            if user is None:
                messages.error(request, 'کاربری با ایمیل وارد شده یافت نشد اگر ثبت نام نکرده اید لطفا ابتدا ثبت نام '
                                        'کنید')
                return redirect('register')
            else:
                mail_subject = 'تغییر رمز عبور'
                message = render_to_string("password_reset_email.html", {
                    'user': user,
                    'domain': get_current_site(request).domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                    'protocol': 'https' if request.is_secure() else 'http'
                })
                email = EmailMessage(mail_subject, message, to=[email_to])
                if email.send():
                    messages.success(request, f"{user} گرامی دستورالعمل بازیابی رمز عبور"
                                              f" به آدرس پست الکترونیک شما {user.email} ارسال شد")
                    return redirect('password-reset')
    else:
        form = ResetPasswordForm()
        return render(request, 'reset_password.html', {'form': form})


@login_required
def password_change_view(request):
    acc = Account.objects.filter(user=request.user).first()
    if request.method == 'POST':
        form = PasswordForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'رمز عبور شما با موفقیت تغییر یافت')
            return redirect('profile')
        return render(request, 'change_password.html', {'form': form, 'acc': acc})
    else:
        form = PasswordForm(request.user)
        return render(request, 'change_password.html', {'form': form, 'acc': acc})


def password_reset_confirm(request, uidb64, token):
    user_model = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = user_model.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, user_model.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        login(request, user)
        return redirect('password-change')
    else:
        messages.error(request, 'متاسفیم لینک وارد شده صحیح نمیباشد یا زمان آن منقضی شده است')
        return redirect('password-reset')
