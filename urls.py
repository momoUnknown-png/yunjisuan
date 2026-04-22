from django.contrib import admin
from django.urls import path
from moments.views import home, show_user, show_status, submit_post
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home),
    path('user/', show_user),
    path('status/', show_status),
    path('post/', submit_post),
]