from django.contrib import admin
from blog import models
# Register your models here.


class Postadmin(admin.ModelAdmin):
    list_display = ['title','create_time','edit_time','category','author']
    fields = ['title','body','excerpt', 'category','author','tags']
    # def save_model(self, request, obj, form, change):
    #     obj.author = request.user
    #     super().save_model(self, request, obj, form, change)


for table in models.__all__[:-1]:
    admin.site.register(getattr(models,table))
admin.site.register(models.Post,Postadmin)
