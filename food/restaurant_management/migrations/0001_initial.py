# Generated by Django 4.1.4 on 2023-04-01 21:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_jalali.db.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('tel', models.CharField(max_length=11, null=True)),
                ('email', models.EmailField(max_length=254, null=True)),
                ('address', models.TextField(null=True)),
                ('acc_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.account')),
            ],
        ),
        migrations.CreateModel(
            name='Deliverer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vehicle_name', models.CharField(max_length=50)),
                ('vehicle_no', models.CharField(max_length=10)),
                ('tel', models.CharField(max_length=11)),
                ('address', models.TextField(null=True)),
                ('avatar', models.ImageField(null=True, upload_to='deliverer/')),
                ('acc_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.account')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Factor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_price', models.PositiveIntegerField()),
                ('p_stat', models.BooleanField(default=False)),
                ('created', django_jalali.db.models.jDateTimeField(auto_now_add=True)),
                ('updated', django_jalali.db.models.jDateTimeField(auto_now=True)),
                ('acc_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.account')),
                ('customer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='restaurant_management.customer')),
                ('deliverer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='restaurant_management.deliverer')),
            ],
            options={
                'ordering': ['created'],
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('cat', models.CharField(choices=[('غذای اصلی', 'غذای اصلی'), ('پیش غذا', 'پیش غذا'), ('دسر', 'دسر'), ('سوپ', 'سوپ'), ('نوشیدنی', 'نوشیدنی'), ('مخلفات', 'مخلفات'), ('سایر', 'سایر')], max_length=20)),
                ('price', models.PositiveIntegerField()),
                ('image', models.ImageField(null=True, upload_to='Items/')),
                ('description', models.TextField(null=True)),
                ('acc_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.account')),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('method', models.CharField(choices=[('اینترنتی', 'اینترنتی'), ('نقدی', 'نقدی'), ('کارتخوان', 'کارتخوان')], max_length=50)),
                ('date', django_jalali.db.models.jDateTimeField(verbose_name='تاریخ')),
                ('description', models.CharField(max_length=100)),
                ('acc_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.account')),
                ('factor', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='restaurant_management.factor')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveSmallIntegerField(default=1)),
                ('created', django_jalali.db.models.jDateTimeField(auto_now_add=True)),
                ('updated', django_jalali.db.models.jDateTimeField(auto_now=True)),
                ('acc_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.account')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='restaurant_management.product')),
            ],
        ),
        migrations.AddField(
            model_name='factor',
            name='orders',
            field=models.ManyToManyField(to='restaurant_management.order'),
        ),
    ]