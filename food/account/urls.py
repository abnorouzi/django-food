from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from account import views


urlpatterns = [
    path('', views.index, name='home'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('register', views.register_view, name='register'),
    path('profile', views.profile_view, name='profile'),
    path('password-reset', views.password_reset_view, name='password-reset'),
    path('password-change', views.password_change_view, name='password-change'),
    path('activate/<uid64>/<token>', views.activate, name='activate'),
    path('reset-confirm/<uidb64>/<token>', views.password_reset_confirm, name='password_reset_confirm'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
