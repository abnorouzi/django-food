from django import forms
from .models import Customer, Product, Deliverer, Order, Factor, Payment


class CustomerForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control bg-warning', 'placeholder':
        'نام و نام خانوادگی'}), min_length=6, max_length=50)
    tel = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control bg-warning', 'placeholder': 'شماره تماس'}
                                                 ), min_length=7, max_length=11, required=False)
    address = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control bg-warning',
                                                           'placeholder': 'آدرس'}), min_length=3, required=False)

    class Meta:
        model = Customer
        fields = ['name', 'tel', 'address']


class ProductForm(forms.ModelForm):
    FOOD_CAT = (
        ('غذای اصلی', 'غذای اصلی'),
        ('پیش غذا', 'پیش غذا'),
        ('دسر', 'دسر'),
        ('سوپ', 'سوپ'),
        ('نوشیدنی', 'نوشیدنی'),
        ('مخلفات', 'مخلفات'),
        ('سایر', 'سایر'),
    )
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control bg-warning', 'placeholder':
        'نام غذا'}), max_length=50)
    cat = forms.ChoiceField(choices=FOOD_CAT)
    price = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control bg-warning', 'placeholder':
        'قیمت غذا'}))
    image = forms.ImageField(required=False)
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control bg-warning', 'placeholder':
        'توضیحات'}), required=False)

    class Meta:
        model = Product
        fields = ['name', 'cat', 'price', 'image', 'description']


class OrderForm(forms.ModelForm):
    product = forms.ModelChoiceField(queryset=Product.objects.all(), widget=forms.Select(attrs={'class': 'form-control bg-warning w-75'}),
                                     empty_label='انتخاب آیتم')
    quantity = forms.CharField(widget=forms.NumberInput(attrs={'class': 'form-control bg-warning w-75', 'placeholder':
        'تعداد', 'value': 1, 'min': 1}))

    class Meta:
        model = Order
        fields = ['product', 'quantity']


class FactorForm(forms.ModelForm):
    customer = forms.ModelChoiceField(queryset=Customer.objects.all(), widget=forms.Select(attrs={'class':
                                                                                                  'form-control w-75'}),
                                      empty_label='انتخاب مشتری')

    class Meta:
        model = Factor
        fields = ['deliverer', 'customer']


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['method', 'description']


class DelivererForm(forms.ModelForm):
    vehicle_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control bg-warning',
                                                                 'placeholder': 'نام وسیله نقلیه'}), min_length=3)
    vehicle_no = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control bg-warning', 'placeholder':
        'پلاک وسیله نقلیه'}), min_length=6, max_length=15)
    tel = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control bg-warning', 'placeholder': 'شماره تماس'}
                                                 ), min_length=7, max_length=11)
    address = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control bg-warning',
                                                            'placeholder': 'آدرس'}), min_length=3)
    avatar = forms.ImageField()

    class Meta:
        model = Deliverer
        fields = ['vehicle_name', 'vehicle_no', 'tel', 'address', 'avatar']
