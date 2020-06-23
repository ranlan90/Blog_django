from django.shortcuts import render,HttpResponse,get_object_or_404,redirect
import markdown
from blog import models
import re
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension
from django.views.generic import ListView, DetailView
from django.views import View
from django.core.paginator import Paginator
from pure_pagination.mixins import PaginationMixin
from django.db.models import Q
from django.contrib import messages


# Create your views here.
def index(request):
    query_set = models.Post.objects.all()
    return render(request,'blog/index.html',{'postlist': query_set})



class IndexView(PaginationMixin,ListView):
    model = models.Post
    template_name = 'blog/index.html'
    context_object_name = 'postlist'
    paginate_by = 5


class SearchView(IndexView):
    def get_queryset(self):
        q = self.request.GET.get('q')
        if not q:
            error_msg = "请输入搜索关键词"
            messages.add_message(self.request, messages.ERROR, error_msg, extra_tags='danger')
        return super(SearchView,self).get_queryset().filter(Q(title__icontains=q)|Q(body__icontains=q))



# class CategoryView(ListView):
#     model = models.Post
#     template_name = 'blog/index.html'
#     context_object_name = 'postlist'
#
#     def get_queryset(self):
#         cate = get_object_or_404(models.Category,pk=self.kwargs.get('pk'))
#         return super(CategoryView,self).get_queryset().filter(category=cate)


class CategoryView(IndexView):
    def get_queryset(self):
        cate = get_object_or_404(models.Category,pk=self.kwargs.get('pk'))
        return super(CategoryView,self).get_queryset().filter(category=cate)


class TagView(View):
    def get(self,request,pk):
        queryset = models.Tag.objects.filter(pk=pk).first()
        if queryset:
            queryset = queryset.post_set.all()
            return render(request,'blog/index.html',{'postlist': queryset})
        else:
            return HttpResponse('url不合法')


class ArchiveView(View):
    def get(self,request,year,month):
        queryset = models.Post.objects.filter(create_time__year=year,create_time__month=month)
        return render(request,'blog/index.html',{'postlist': queryset})




def detail(request,pk):
    post = get_object_or_404(models.Post, pk=pk)
    post.increase_views()
    # md = markdown.Markdown(extensions=[
    #     'markdown.extensions.extra',
    #     'markdown.extensions.fenced_code',
    #     TocExtension(slugify=slugify),
    # ])
    # post.body = md.convert(post.body)
    # m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
    # post.toc = m.group(1) if m is not None else ''

    return render(request,'blog/detail.html',{'post': post})


class PostDetailView(DetailView):
    # 这些属性的含义和 ListView 是一样的
    model = models.Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'
    def get(self,request,*args, **kwargs):

        response = super(PostDetailView, self).get(request,*args, **kwargs)
        self.object.increase_views()
        return response

    # def get_object(self, queryset=None):
    #     post = super(PostDetailView, self).get_object(queryset=None)
    #     md = markdown.Markdown(extensions=[
    #         'markdown.extensions.extra',
    #         'markdown.extensions.fenced_code',
    #         TocExtension(slugify=slugify),
    #     ])
    #     post.body = md.convert(post.body)
    #     m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
    #     post.toc = m.group(1) if m is not None else ''
    #     return post


class Full_width(IndexView):
    template_name = 'blog/full-width.html'



def about(request):
    return render(request,'blog/about.html')


def contact(request):
    return render(request,'blog/contact.html')
