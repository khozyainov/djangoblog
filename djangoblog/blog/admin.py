from django.contrib import admin
from .models import Author, Blog
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
# Register your models here.

admin.site.register(Author)

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'post_date')
    list_filter = ('post_date',)


class EmailRequiredMixin(object):
    def __init__(self, *args, **kwargs):
        super(EmailRequiredMixin, self).__init__(*args, **kwargs)
        # make user email field required
        self.fields['email'].required = True


class UserWithEmailCreationForm(EmailRequiredMixin, UserCreationForm):
    pass


class UserWithEmailChangeForm(EmailRequiredMixin, UserChangeForm):
    pass


class EmailRequiredUserAdmin(UserAdmin):
    form = UserWithEmailChangeForm
    add_form = UserWithEmailCreationForm
    add_fieldsets = ((None, {
        'fields': ('username', 'email', 'password1', 'password2'),
        'classes': ('wide',)
    }),)


admin.site.unregister(User)
admin.site.register(User, EmailRequiredUserAdmin)
