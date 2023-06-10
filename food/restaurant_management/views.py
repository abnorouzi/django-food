import json
from django.utils.safestring import mark_safe
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from account.models import Account
from account.forms import RegisterForm
from .forms import *
from .models import *
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist


@login_required
def home_view(request):
    acc = Account.objects.filter(user=request.user).first()
    return render(request, 'restaurant.html', {'acc': acc, 'd': jdatetime.datetime.today()})


@login_required
def deliverer_view(request):
    acc = Account.objects.filter(user=request.user).first()
    user_form = RegisterForm()
    deliver_form = DelivererForm()
    deliverer = Deliverer.objects.all()
    context = {
        "user_stat": "active",
        "user_open": "menu-open",
        'acc': acc,
        'user_form': user_form,
        'deliver_form': deliver_form,
        'deliverer': deliverer,
        'd': jdatetime.datetime.today()
    }
    if request.method == 'POST':
        deliver_form = DelivererForm(request.POST, request.FILES)
        user_form = RegisterForm(request.POST)
        avatar = request.FILES['avatar']
        if user_form.is_valid() and deliver_form.is_valid():
            dcd = deliver_form.cleaned_data
            ucd = user_form.cleaned_data
            first = ucd['first_name']
            last = ucd['last_name']
            username = ucd['username']
            password = ucd['password1']
            em = ucd['email']
            u = User.objects.create_user(username=username, password=password, email=em)
            u.first_name = first
            u.last_name = last
            u.save()
            vNo = dcd['vehicle_no']
            vName = dcd['vehicle_name']
            tel = dcd['tel']
            address = dcd['address']
            de = Deliverer.objects.create(user=u, vehicle_name=vName, vehicle_no=vNo, tel=tel, address=address,
                                          avatar=avatar, acc_id=acc)
            de.save()
            if de and de is not None:
                messages.success(request, 'کاربر جدید افزوده شد')
                return redirect('res_admin')
            else:
                messages.success(request, 'متاسفانه خطایی رخ داد لطفا دوباره تلاش کنید')
                return redirect('res_admin')
        else:
            messages.success(request, "متاسفانه خطایی رخ داد لطفا دوباره تلاش کنید")
            return redirect('res_admin')
    else:
        return render(request, 'pages/deliverer.html', context)


@login_required
def update_deliverer(request, did):
    if request.method == 'POST':
        r = request.POST
        d = Deliverer.objects.filter(id=did).first()
        d.avatar = request.FILES['avatar']
        d.first_name = r['first_name']
        d.last_name = r['last_name']
        d.username = r['username']
        d.email = r['email']
        d.vehicle_name = r['vehicle_name']
        d.vehicle_no = r['vehicle_no']
        d.tel = r['tel']
        d.address = r['address']
        d.save()
        return redirect('res_deliverer')
    else:
        return render(request, '404.html')


@login_required
def del_deliverer(request, did):
    Deliverer.objects.filter(id=did).delete()
    return redirect('res_deliverer')


@login_required
def tables_view(request):
    acc = Account.objects.filter(user=request.user).first()
    context = {
        "table_stat": "active",
        'acc': acc,
        'd': jdatetime.datetime.today(),
    }
    return render(request, 'pages/tables.html', context)


@login_required
def food_view(request):
    acc = Account.objects.filter(user=request.user).first()
    items = Product.objects.all()
    form = ProductForm()
    context = {
        "item_stat": "active",
        "item_open": "menu-open",
        'acc': acc,
        'form': form,
        'items': items,
        'd': jdatetime.datetime.today(),
    }
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            cd = form.cleaned_data
            name = cd['name']
            cat = cd['cat']
            price = cd['price']
            image = cd['image']
            des = cd['description']
            food = Product.objects.create(name=name, cat=cat, price=price, image=image, description=des, acc_id=acc)
            food.save()
            messages.success(request, 'غذا افزوده شد')
            return redirect('res_food')
        else:
            messages.error(request, str(form.errors) + 'متاسفیم خطایی رخ داد لطفا دوباره تلاش کنید ')
            return redirect('res_food')
    else:
        return render(request, 'pages/food.html', context)


@login_required
def update_food(request, fid):
    acc = Account.objects.filter(user=request.user).first()
    item = Product.objects.filter(id=fid).first()
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            cd = form.cleaned_data
            item.name = cd['name']
            item.cat = cd['cat']
            item.price = cd['price']
            item.image = cd['image']
            item.description = cd['description']
            item.save()
            messages.success(request, 'آیتم مورد نظر با موفقیت تغییر یافت')
            return redirect('res_food')
        else:
            messages.error(request, str(form.errors) + 'متاسفیم خطایی رخ داد لطفا دوباره تلاش کنید ')
            return redirect('res_food')
    else:
        form = ProductForm(initial={"name": item.name, "cat": item.cat, "price": item.price,
                                    "image": item.image, "description": item.description})
        return render(request, 'pages/food.html', {'acc': acc, 'form': form, "item_stat": "active",
                                                   "item_open": "menu-open"})


@login_required
def del_food(request, fid):
    Product.objects.filter(id=fid).first().delete()
    messages.warning(request, 'آیتم مورد نظر با موفقیت حذف شد')
    return redirect('res_food')


@login_required
def create_factor(request):
    acc = Account.objects.filter(user=request.user).first()
    factor = Factor.objects.create(acc_id=acc)
    request.session['fac_tor'] = factor.id
    messages.warning(request, 'یک فاکتور جدید ایجاد شد')
    return redirect('res_order')


@login_required
def order_view(request):
    acc = Account.objects.filter(user=request.user).first()
    if request.method == 'POST':
        form = OrderForm(request.POST)
        fid = request.POST['facid']
        if form.is_valid():
            cd = form.cleaned_data
            factor = Factor.objects.filter(id=fid).get()
            if factor.complete:
                del request.session['fac_tor']
                return render(request, 'payment.html')
            else:
                order = Order.objects.create(product=cd['product'], quantity=cd['quantity'], acc_id=acc)
                factor.orders.add(order)
                factor.save()
                request.session['fac_tor'] = factor.id
                return redirect('res_order')
        messages.error(request, 'متاسفیم خطایی رخ داد')
        return redirect('res_order')
    else:
        form = OrderForm()
        customers = Customer.objects.all()
        fac_id = 0
        if request.session.has_key('fac_tor'):
            fac_id = request.session['fac_tor']
            del request.session['fac_tor']
        context = {
            "order_stat": "active",
            "order_open": "menu-open",
            'acc': acc,
            'form': form,
            'd': jdatetime.datetime.today(),
            'c': customers,
        }
        try:
            factor = Factor.objects.filter(id=fac_id).get()
            context['factor'] = factor
            return render(request, 'pages/order.html', context)
        except ObjectDoesNotExist:
            return render(request, 'pages/order.html', context)


@login_required
def del_order(request, fid, oid):
    factor = Factor.objects.filter(id=fid).get()
    order = Order.objects.filter(id=oid).get()
    factor.orders.remove(order)
    factor.save()
    request.session['fac_tor'] = factor.id
    return redirect('res_order')


@login_required
def del_factor(request, fid):
    Factor.objects.filter(id=fid).delete()
    return redirect('res_order')


@login_required
def pending_view(request):
    acc = Account.objects.filter(user=request.user).first()
    customers = Customer.objects.filter(acc_id=acc).all()
    context = {
        "order_stat": "active",
        "order_open": "menu-open",
        'acc': acc,
        'd': jdatetime.datetime.today(),
        'customers': customers,
    }
    if request.method == 'POST':
        sid = request.POST.get('search_id')
        name = request.POST.get('search_name')
        c = Customer.objects.filter(name=name)
        start_dt = request.POST.get('start_dt')
        end_dt = request.POST.get('end_dt')
        fac_date = object()
        fac_endless = object()
        if start_dt and end_dt:
            st = jdatetime.JalaliToGregorian(int(start_dt[:4]), int(start_dt[5:7]), int(start_dt[8:]))
            ed = jdatetime.JalaliToGregorian(int(end_dt[:4]), int(end_dt[5:7]), int(end_dt[8:]))
            fac_date = Factor.objects.filter(created__date__range=(datetime.date(st.gyear, st.gmonth, st.gday),
                                                                   datetime.date(ed.gyear, ed.gmonth,
                                                                                 ed.gday))).all()
            dt_now = datetime.date.today()
            fac_endless = Factor.objects.filter(
                created__date__range=(datetime.date(st.gyear, st.gmonth, st.gday), dt_now)).all()
        if request.POST.get('not_paid') == 'on':
            if c:
                if start_dt and end_dt:
                    try:
                        factor = fac_date.filter(customer__in=c).all()
                        context['factor'] = factor
                    except ObjectDoesNotExist:
                        return redirect('404')
                elif start_dt:
                    factor = fac_endless.filter(customer__in=c).all()
                    context['factor'] = factor
                else:
                    factor = Factor.objects.filter(customer__in=c).all()
                    context['factor'] = factor
            else:
                if start_dt and end_dt:
                    factor = fac_date.all()
                    context['factor'] = factor
                elif start_dt:
                    factor = fac_endless.all()
                    context['factor'] = factor
                else:
                    factor = Factor.objects.all()
                    context['factor'] = factor
        else:
            if sid:
                try:
                    factor = Factor.objects.filter(id=sid)
                    context['factor'] = factor
                except ObjectDoesNotExist:
                    redirect('404')
            else:
                if c:
                    if start_dt and end_dt:
                        factor = fac_date.filter(customer__in=c).all()
                        context['factor'] = factor
                    elif start_dt:
                        factor = fac_endless.filter(customer__in=c).all()
                        context['factor'] = factor
                    else:
                        factor = Factor.objects.filter(customer=c).all()
                        context['factor'] = factor
                else:
                    if start_dt and end_dt:
                        factor = fac_date.all()
                        context['factor'] = factor
                    elif start_dt:
                        factor = fac_endless.all()
                        context['factor'] = factor
                    else:
                        factor = Factor.objects.all()
                        context['factor'] = factor
        return render(request, 'pages/order-pending.html', context)
    return render(request, 'pages/order-pending.html', context)


@login_required
def customers_view(request):
    acc = Account.objects.filter(user=request.user).first()
    customers = Customer.objects.all()
    form = CustomerForm()
    context = {
        "user_stat": "active",
        "user_open": "menu-open",
        'acc': acc,
        'form': form,
        'customers': customers,
        'd': jdatetime.datetime.today(),
    }
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            name = cd['name']
            tel = cd['tel']
            address = cd['address']
            customer = Customer.objects.create(name=name, tel=tel, address=address, acc_id=acc)
            customer.save()
            messages.success(request, 'مشتری افزوده شده')
            return redirect('res_customers')
        else:
            messages.error(request, 'متاسفیم خطایی رخ داد لطفا دوباره تلاش کنید')
            return redirect('res_customers')
    else:
        return render(request, 'pages/customers.html', context)


@login_required
def update_customer(request, cid):
    c = Customer.objects.filter(id=cid).first()
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            c.name = cd['name']
            c.tel = cd['tel']
            c.address = cd['address']
            c.save()
            messages.success(request, 'مشتری تغییر یافت')
            return redirect('res_customers')
        else:
            messages.error(request, 'متاسفیم خطایی رخ داد لطفا دوباره تلاش کنید')
    else:
        return render(request, '404.html')


@login_required
def del_customer(request, cid):
    if request.method == 'POST':
        Customer.objects.filter(id=cid).delete()
        return redirect('res_customers')
    else:
        return render(request, '404.html')


@login_required
def sale_view(request):
    acc = Account.objects.filter(user=request.user).first()
    data = get_chart_values()
    labels = ["فروردین", "اردیبهشت", "خرداد", "تیر", "مرداد", "شهریور", "مهر", "آبان", "آذر", "دی", "بهمن", "اسفند"]
    context = {
        "report_stat": "active",
        "report_open": "menu-open",
        'acc': acc,
        'd': jdatetime.datetime.today(),
        'labels': mark_safe(json.dumps(labels)),
        'data': mark_safe(json.dumps(data)),
    }
    return render(request, 'pages/sale.html', context)


@login_required
def best_food_view(request):
    acc = Account.objects.filter(user=request.user).first()
    products = Product.objects.all()
    data = []
    labels = []
    context = {
        "report_stat": "active",
        "report_open": "menu-open",
        'acc': acc,
        'd': jdatetime.datetime.today(),
        'products': products
    }
    if request.method == 'POST':
        start_dt = request.POST.get('start_dt')
        end_dt = request.POST.get('end_dt')
        dt = datetime.date.today()
        dic = {}
        for p in products:
            dic[p.name] = 0
        if start_dt and end_dt:
            st = jdatetime.JalaliToGregorian(int(start_dt[:4]), int(start_dt[5:7]), int(start_dt[8:]))
            ed = jdatetime.JalaliToGregorian(int(end_dt[:4]), int(end_dt[5:7]), int(end_dt[8:]))
            fac_date = Factor.objects.filter(created__date__range=(datetime.date(st.gyear, st.gmonth, st.gday),
                                                                   datetime.date(ed.gyear, ed.gmonth,
                                                                                 ed.gday))).all()
            for factor in fac_date:
                for order in factor.orders.all():
                    for p in products:
                        if p.name == order.product.name:
                            dic[p.name] = dic[p.name] + order.quantity
        else:
            fac_date = Factor.objects.filter(created__date__range=(datetime.date(dt.year, dt.month, 1), dt)).all()
            for factor in fac_date:
                for order in factor.orders.all():
                    for p in products:
                        if p.name == order.product.name:
                            dic[p.name] = dic[p.name] + order.quantity

        for d in dic.values():
            data.append(d)
        for i in dic.keys():
            labels.append(i)
        context['labels'] = mark_safe(json.dumps(labels))
        context['data'] = mark_safe(json.dumps(data))
        return render(request, 'pages/best_food.html', context)
    else:
        return render(request, 'pages/best_food.html', context)


@login_required
def best_customer_view(request):
    acc = Account.objects.filter(user=request.user).first()
    context = {
        "report_stat": "active",
        "report_open": "menu-open",
        'acc': acc,
        'd': jdatetime.datetime.today(),
    }
    return render(request, 'pages/best_customers.html', context)


@login_required
def print_factor(request, fid):
    factor = Factor.objects.filter(id=fid)
    context = {
        'factor': factor
    }
    return render(request, 'print.html', context)
