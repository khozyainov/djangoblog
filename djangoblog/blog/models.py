from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.core.mail import send_mass_mail


# Create your models here.
class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    following = models.ManyToManyField('Author', related_name='followers', null=True, blank=True)

    class Meta:
        ordering = ["user"]

    def get_absolute_url(self):
        return reverse('blogs-by-author', args=[str(self.id)])

    def __str__(self):
        return self.user.username

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Author.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.author.save()

class Blog(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True)
    text = models.TextField()
    post_date = models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering = ['-post_date']

    def get_absolute_url(self):
        return reverse('blog-detail', args=[str(self.id)])

    def __str__(self):
        return self.title


@receiver(post_save, sender=Blog)
def first_mail(sender, instance, **kwargs):
    if kwargs['created']:
        messages = tuple()
        author = Author.objects.get(user=instance.author.user)
        post_url = '127.0.0.1:8000' + instance.get_absolute_url()
        for follower in author.following.all():
            email_to = follower.user.email
            message = ('New post on Django Blog',
                       f'Hey, here new post ({post_url})',
                       'from@djangoblog.com',
                       [f'{email_to}'],)
            messages += (message,)
        send_mass_mail(messages)
