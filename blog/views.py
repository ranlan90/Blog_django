from django.shortcuts import render,HttpResponse,get_object_or_404
import markdown
from blog import models
import re
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension

# Create your views here.
def index(request):
    query_set = models.Post.objects.all()
    return render(request,'blog/index.html',{'postlist': query_set})


def detail(request,pk):
    post = get_object_or_404(models.Post, pk=pk)
    md = markdown.Markdown(extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.fenced_code',
        TocExtension(slugify=slugify),
    ])
    post.body = md.convert(post.body)
    m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
    post.toc = m.group(1) if m is not None else ''

    return render(request,'blog/detail.html',{'post': post})
