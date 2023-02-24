"""sandbox URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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

from django.http import HttpResponse


# def home(request):
#     # rooms = [
#     #     {'id':1, 'name':'Lets learn Python!'},
#     #     {'id':2, 'name':'Design with me'},
#     #     {'id':3, 'name':'Data scientists!'},
#     # ]
#     # return render(request, 'forum/home.html', {'context': rooms})
#     return HttpResponse('HELLO')


urlpatterns = [
    path('', include('forum.urls')),
    # path('', home),
    path('admin/', admin.site.urls),
]
