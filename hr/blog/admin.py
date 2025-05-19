from django.contrib import admin

from blog.models import Post

@admin.register(Post)
class MyModelAdmin(admin.ModelAdmin):
    exclude = ['date']