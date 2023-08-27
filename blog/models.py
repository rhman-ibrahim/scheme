# Django
from django.db import models
from django.urls import reverse

# MPTT
from mptt.models import MPTTModel, TreeForeignKey

# Helpers
from helpers.functions import generate_identifier


class Signal(models.Model):

    classification = models.CharField(max_length=64, default="signal", blank=False, null=False)
    glyph          = models.CharField(max_length=64, default="material-symbols-outlined")
    icon           = models.CharField(max_length=64, default="radio_button_checked")
    
    def __str__(self):
        return self.classification

class SignalBase(models.Model):
    
    space          = models.ForeignKey("team.Space", on_delete=models.CASCADE)
    signal         = models.ForeignKey("blog.Signal", default=16, on_delete=models.CASCADE)
    user           = models.ForeignKey("user.Account", on_delete=models.CASCADE, default=None, blank=True, null=True)
    identifier     = models.CharField(max_length=64, default=generate_identifier, null=False, blank=False, editable=False)
    status         = models.BooleanField(default=True, blank=False, null=False)
    created        = models.DateTimeField(auto_now_add=True)
    updated        = models.DateTimeField(auto_now=True)
        
    def get_status(self):
        return {
            'i': "radio_button_checked" if self.status == 1 else "check_circle",
            'c': "primary" if self.status == 1 else "success",
            'v': "opened" if self.status == 1 else "closed"
        }
    
    def beam(self):
        query = self.get_descendants(include_self=True).filter(level__lte=self.level+1, user=self.user)
        return query if query.count() > 1 else None
    
    class Meta:
        abstract = True
    
class Post(SignalBase, MPTTModel):

    parent         = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    body           = models.TextField(max_length=512, blank=False, null=False)

    def __str__(self):
        return f"{self.signal.classification} post by {self.user.username}"

    def url(self):
        return reverse("blog:retrieve_post", args=[str(self.identifier)])
    
    def comments(self):
        query = Comment.objects.filter(
            pk__in=[comment.id for comment in Comment.objects.filter(post=self) if comment.user != self.user]
        )
        return query if query.count() else None

class Comment(SignalBase, MPTTModel):

    post           = models.ForeignKey("blog.Post", on_delete=models.CASCADE)
    parent         = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    body           = models.TextField(max_length=512, blank=False, null=False)

    def __str__(self):
        return f"{self.signal.classification} comment by {self.user.username}"
    
    def url(self):
        return reverse("blog:retrieve_comment", args=[str(self.identifier)])
    
    def replies(self):
        query = Comment.objects.filter(
            pk__in=[comment.id for comment in self.get_children() if comment.user != self.user]
        )
        return query if query.count() else None