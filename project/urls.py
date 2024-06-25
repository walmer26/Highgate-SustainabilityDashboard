"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from allauth.account.decorators import secure_admin_login



admin.autodiscover()
admin.site.login = secure_admin_login(admin.site.login)


# This class provides a home page when no app is added.
# Index template is part of the AllAuth html files.
class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "index.html"


urlpatterns = [
    # Django
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),

    # Debug-Toolbar
    path('__debug__/', include('debug_toolbar.urls')),\
    
    # AllAuth
    path('accounts/', include('allauth.urls')),
    path("", HomeView.as_view(template_name="index.html"), name='index'),

    # MyApps
    path('users/', include('apps.users.urls', namespace='users')),
    path('dashboard/', include('apps.dashboard.urls', namespace='dashboard')),
]
