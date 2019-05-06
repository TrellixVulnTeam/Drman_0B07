from django.contrib import admin
from .models import Post , Comments , Categories


class PostAdmin(admin.ModelAdmin) :
    search_fields = ('title', 'body')
    prepopulated_fields = {"slug": ("title",)}



admin.site.register(Post, PostAdmin)


class CommentsAdmin(admin.ModelAdmin) :
    list_display = ('name', 'email', 'post' , 'created' , 'active')
    list_filter = ('active', 'post', 'created', 'updated')
    search_fields = ('name', 'email', 'body')


admin.site.register(Comments, CommentsAdmin)


class CategoryAdmin(admin.ModelAdmin):
    search_fields = ['name', 'slug']
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(Categories, CategoryAdmin)
