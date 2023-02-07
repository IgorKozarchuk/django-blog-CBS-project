from django.contrib import admin

from .models import *


# Register your models here.
class CommentInline(admin.StackedInline):
	model = Comment
	extra = 1 # number of extra empty comments


class PostAdmin(admin.ModelAdmin):
	inlines = [
		CommentInline,
	]


admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
