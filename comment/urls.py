

from django.urls import path,re_path
from comment import views


app_name = 'comments'
urlpatterns = [
    re_path('^comment/(?P<post_pk>\d+)',views.comment,name='comment_add'),
]
