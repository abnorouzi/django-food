import datetime

import jdatetime
from django_jalali.db import models as jmodels
from django.contrib.auth.models import User
from django.db import models
from account.models import Account


class Customer(models.Model):
    name = models.CharField(max_length=50)
    tel = models.CharField(max_length=11, null=True)
    email = models.EmailField(null=True)
    address = models.TextField(null=True)
    acc_id = models.ForeignKey(Account, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Product(models.Model):
    FOOD_CAT = (
        ('غذای اصلی', 'غذای اصلی'),
        ('پیش غذا', 'پیش غذا'),
        ('دسر', 'دسر'),
        ('سوپ', 'سوپ'),
        ('نوشیدنی', 'نوشیدنی'),
        ('مخلفات', 'مخلفات'),
        ('سایر', 'سایر'),
    )
    name = models.CharField(max_length=50)
    cat = models.CharField(max_length=20, choices=FOOD_CAT)
    price = models.PositiveIntegerField()
    image = models.ImageField(upload_to='Items/', null=True)
    description = models.TextField(null=True)
    acc_id = models.ForeignKey(Account, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Deliverer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vehicle_name = models.CharField(max_length=50)
    vehicle_no = models.CharField(max_length=10)
    tel = models.CharField(max_length=11)
    address = models.TextField(null=True)
    avatar = models.ImageField(upload_to='deliverer/', null=True)
    acc_id = models.ForeignKey(Account, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user) + " Delivery"


class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created = jmodels.jDateTimeField(auto_now_add=True)
    updated = jmodels.jDateTimeField(auto_now=True)
    acc_id = models.ForeignKey(Account, on_delete=models.CASCADE)

    def __str__(self):
        return "Order_" + str(self.created)

    def get_total_price(self):
        return self.product.price * self.quantity


class Factor(models.Model):
    orders = models.ManyToManyField(Order)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    deliverer = models.ForeignKey(Deliverer, on_delete=models.SET_NULL, null=True, blank=True)
    p_stat = models.BooleanField(default=False)
    complete = models.BooleanField(default=False)
    created = jmodels.jDateTimeField(auto_now_add=True)
    updated = jmodels.jDateTimeField(auto_now=True)
    acc_id = models.ForeignKey(Account, on_delete=models.CASCADE)

    class Meta:
        ordering = ['created']

    def __str__(self):
        return "Factor-" + str(self.created)

    def get_total_price(self):
        ords = self.orders.all()
        total = 0
        for order in ords:
            total += order.get_total_price()
        return total

    def get_payment(self):
        if self.p_stat:
            return "پرداخت شده"
        else:
            return "پرداخت نشده"


class Payment(models.Model):
    METHOD = (
        ('اینترنتی', 'اینترنتی'),
        ('نقدی', 'نقدی'),
        ('کارتخوان', 'کارتخوان'),
    )
    factor = models.ForeignKey(Factor, on_delete=models.PROTECT)
    method = models.CharField(max_length=50, choices=METHOD)
    date = jmodels.jDateTimeField(verbose_name='تاریخ')
    description = models.CharField(max_length=100)
    acc_id = models.ForeignKey(Account, on_delete=models.CASCADE)

    def __str__(self):
        return "Payment" + str(self.date)


def get_chart_values():
    values = []
    dt = datetime.date.today()
    fac_date = Factor.objects.filter(created__date__range=(datetime.date(dt.year, 3, 21), datetime.date(dt.year, 4, 21))).all()
    t = 0
    for v in fac_date:
        t += v.get_total_price()
    values.append(t)
    t = 0
    fac_date = Factor.objects.filter(created__date__range=(datetime.date(dt.year, 4, 21), datetime.date(dt.year, 5, 22))).all()
    for v in fac_date:
        t += v.get_total_price()
    values.append(t)
    fac_date = Factor.objects.filter(created__date__range=(datetime.date(dt.year, 5, 22), datetime.date(dt.year, 6, 22))).all()
    t = 0
    for v in fac_date:
        t += v.get_total_price()
    values.append(t)
    fac_date = Factor.objects.filter(created__date__range=(datetime.date(dt.year, 6, 22), datetime.date(dt.year, 7, 23))).all()
    t = 0
    for v in fac_date:
        t += v.get_total_price()
    values.append(t)
    fac_date = Factor.objects.filter(created__date__range=(datetime.date(dt.year, 7, 23), datetime.date(dt.year, 8, 23))).all()
    t = 0
    for v in fac_date:
        t += v.get_total_price()
    values.append(t)
    fac_date = Factor.objects.filter(created__date__range=(datetime.date(dt.year, 8, 23), datetime.date(dt.year, 9, 23))).all()
    t = 0
    for v in fac_date:
        t += v.get_total_price()
    values.append(t)
    fac_date = Factor.objects.filter(created__date__range=(datetime.date(dt.year, 9, 23), datetime.date(dt.year, 10, 23))).all()
    t = 0
    for v in fac_date:
        t += v.get_total_price()
    values.append(t)
    fac_date = Factor.objects.filter(created__date__range=(datetime.date(dt.year, 10, 23), datetime.date(dt.year, 11, 22))).all()
    t = 0
    for v in fac_date:
        t += v.get_total_price()
    values.append(t)
    fac_date = Factor.objects.filter(created__date__range=(datetime.date(dt.year, 11, 22), datetime.date(dt.year, 12, 22))).all()
    t = 0
    for v in fac_date:
        t += v.get_total_price()
    values.append(t)
    fac_date = Factor.objects.filter(created__date__range=(datetime.date(dt.year, 12, 22), datetime.date(dt.year, 1, 21))).all()
    t = 0
    for v in fac_date:
        t += v.get_total_price()
    values.append(t)
    fac_date = Factor.objects.filter(created__date__range=(datetime.date(dt.year, 1, 21), datetime.date(dt.year, 2, 20))).all()
    t = 0
    for v in fac_date:
        t += v.get_total_price()
    values.append(t)
    fac_date = Factor.objects.filter(created__date__range=(datetime.date(dt.year, 2, 20), datetime.date(dt.year, 3, 21))).all()
    t = 0
    for v in fac_date:
        t += v.get_total_price()
    values.append(t)
    return values


