from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password

from .models import Account

err = {
    'required': 'پرکردن این فیلد اجباری است',
    'invalid': 'مقدار وارد شده صحیح نمیباشد',
    'min_length': 'کاراکترهای ورودی کمتر از حد مجاز است',
    'unique': 'این نام کاربری موجود میباشد لطفا یک نام دیگر انتخاب کنید'
}


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control bg-warning', 'placeholder': 'نام کاربری'}),
        error_messages=err)
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control bg-warning', 'placeholder': 'رمز عبور'}),
        error_messages=err)


class PasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control bg-warning', 'placeholder': 'رمز عبور جدید'}),
        error_messages=err, validators=[validate_password])
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control bg-warning', 'placeholder': 'تکرار رمز عبور'}),
        error_messages={"password_mismatch": "رمز عبور شما هم خوانی ندارد"}, validators=[validate_password])

    class Meta:
        model = get_user_model()
        fields = ['new_password1', 'new_password2']


class ResetPasswordForm(PasswordResetForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control bg-warning', 'placeholder': 'پست الکترونیک'}),
        error_messages=err, min_length=9)

    class Meta:
        model = get_user_model()
        fields = []


class RegisterForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control bg-warning', 'placeholder': 'نام کاربری'}),
        error_messages=err, min_length=3)
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control bg-warning', 'placeholder': 'رمز عبور'}),
        error_messages=err, validators=[validate_password])
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control bg-warning', 'placeholder': 'تکرار رمز عبور'}),
        error_messages=err, validators=[validate_password])
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control bg-warning', 'placeholder': 'نام'}),
        error_messages=err, min_length=3)
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control bg-warning', 'placeholder': 'نام خانوادگی'}),
        error_messages=err, min_length=4)
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control bg-warning', 'placeholder': 'پست الکترونیک'}),
        error_messages=err, min_length=9)

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'first_name', 'last_name', 'email')


class AccountForm(forms.ModelForm):
    CATEGORY = (
        ('restaurant', 'رستوران'),
        ('pizza', 'پیتزا'),
        ('coffeeshop', 'کافی شاپ'),
        ('other', 'سایر'),
    )
    company = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control bg-warning', 'placeholder': 'نام شرکت'}), required=False)
    tel = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control bg-warning', 'placeholder':
                          'شماره تماس'}), required=False)
    avatar = forms.FileField(widget=forms.FileInput(attrs={'class': 'form-control bg-warning', 'placeholder':
                             'عکس پروفایل'}), required=False)
    logo = forms.FileField(widget=forms.FileInput(attrs={'class': 'form-control bg-warning', 'placeholder': 'لوگو'}),
                           required=False)
    address = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control bg-warning', 'placeholder': 'آدرس'})
                              , required=False)
    cat = forms.ChoiceField(choices=CATEGORY, label="انتخاب گروه کاری")

    class Meta:
        model = Account
        fields = ['company', 'tel', 'avatar', 'logo', 'address', 'cat']
