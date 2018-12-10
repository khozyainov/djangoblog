from django.contrib import admin
from .models import Author, Blog

# Register your models here.

admin.site.register(Author)
#admin.site.register(Blog)


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'post_date')
    list_filter = ('post_date',)
