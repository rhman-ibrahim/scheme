# Django
from django.db import models
from django.urls import reverse

# MPTT
from mptt.models import MPTTModel, TreeForeignKey

# Helpers
from helpers.functions import generate_serial


class Signal(MPTTModel):

    # Parent
    parent         = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    # Creator & Contributor
    owner          = models.ForeignKey("user.Account", on_delete=models.CASCADE, blank=False, null=False, related_name="owner")
    user           = models.ForeignKey("user.Account", on_delete=models.CASCADE, default=None, blank=True, null=True, related_name="user")
    # Identification
    circle         = models.ForeignKey("team.Circle", on_delete=models.CASCADE)
    classification = models.CharField(max_length=64, default="signal", blank=False, null=False)
    glyph          = models.CharField(max_length=64, default="material-symbols-outlined")
    icon           = models.CharField(max_length=64, default="radio_button_checked")
    # Room
    serial         = models.CharField(max_length=64, default=generate_serial, null=False, blank=False, editable=False)
    status         = models.BooleanField(default=False, blank=False, null=False)
    # Value    
    body           = models.TextField(max_length=512, blank=False, null=False)
    created        = models.DateTimeField(auto_now_add=True)
    updated        = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.serial}"

    def url(self):
        return reverse("blog:get_signal", args=[str(self.serial)])
    
    def get_status_icon(self):
        if self.status == 0: return "line_start_circle"
        return "line_end_circle"
    
    def update_status(self):
        return reverse("blog:update_signal_status", args=[str(self.serial)])