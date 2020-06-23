from django.shortcuts import render,redirect,reverse
from comment import models,forms
from django.contrib import messages

# Create your views here.


def comment(request,post_pk):
    post = models.Post.objects.filter(pk=post_pk).first()
    instance = models.Comment(post=post)
    form_obj = forms.CommentForm(request.POST, instance=instance)
    if request.method == 'POST':
        if form_obj.is_valid():
            comment_obj = form_obj.save()
            messages.add_message(request,messages.SUCCESS,'发表评论成功',extra_tags='success')
            return redirect(post.get_absolute_url())
        # 检查到数据不合法，我们渲染一个预览页面，用于展示表单的错误。
        # 注意这里被评论的文章 post 也传给了模板，因为我们需要根据 post 来生成表单的提交地址。
        messages.add_message(request, messages.ERROR, '评论发表失败！请修改表单中的错误后重新提交。', extra_tags='danger')
        return render(request,'comment/preview.html',{'post':post,'form_obj':form_obj})




