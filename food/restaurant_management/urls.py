from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from restaurant_management import views

urlpatterns = [
    path('', views.home_view, name='res_admin'),
    path('deliverer', views.deliverer_view, name='res_deliverer'),
    path('update-deliverer/<did>', views.update_deliverer, name='update_deliverer'),
    path('del-deliverer/<did>', views.del_deliverer, name='del_deliverer'),
    path('tables', views.tables_view, name='res_tables'),
    path('food', views.food_view, name='res_food'),
    path('update-food/<fid>', views.update_food, name='update_food'),
    path('del-food/<fid>', views.del_food, name='del_food'),
    path('order', views.order_view, name='res_order'),
    path('create-factor', views.create_factor, name='create_factor'),
    path('order-pending', views.pending_view, name='res_pending'),
    path('del_factor/<fid>', views.del_factor, name='del_factor'),
    path('del_order/<fid>/<oid>', views.del_order, name='del_order'),
    path('customers', views.customers_view, name='res_customers'),
    path('update-customer/<cid>', views.update_customer, name='update_customer'),
    path('del-customer/<cid>', views.del_customer, name='del_customer'),
    path('sale', views.sale_view, name='res_sale'),
    path('best_customer', views.best_customer_view, name='res_best_customer'),
    path('best_food', views.best_food_view, name='res_best_food'),
    path('print_factor/<fid>', views.print_factor, name='print_factor'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
