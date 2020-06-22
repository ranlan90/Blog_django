from django.urls import path,re_path
from blog import views

app_name ='blog'
urlpatterns = [
    # path('', views.index,name='index'),
    path('', views.IndexView.as_view(),name='index'),
    # re_path('^post/(?P<pk>\d+)', views.detail,name='detail'),
    re_path('^post/(?P<pk>\d+)', views.PostDetailView.as_view(),name='detail'),
    re_path('^categories/(?P<pk>\d+)', views.CategoryView.as_view(),name='category'),
    re_path('^tags/(?P<pk>\d+)', views.TagView.as_view(),name='tag'),
    re_path('^search/', views.SearchView.as_view(),name='search'),
    # re_path('^archives/(?P<year>\d+)/(?P<month>\d+)', views.ArchiveView.as_view(),name='archive'),
    path('archives/<int:year>/<int:month>/', views.ArchiveView.as_view(),name='archive'),

]
