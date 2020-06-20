from django.urls import path,re_path
from blog import views

app_name ='blog'
urlpatterns = [
    path('', views.index,name='index'),
    re_path('^post/(?P<pk>\d+)', views.detail,name='detail'),
]
