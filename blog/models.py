# Django
from django.db import models
from django.urls import reverse
# MPTT
from mptt.models import MPTTModel, TreeForeignKey
# Helpers
from helpers.functions import generate_serial


SIGNAL_CLASSIFICATION = (
    (1, "Comment"),
    (2, "Criteria"),
    (3, "Decision"),
    (4, "Hypothesis"),
    (5, "Insight"),
    (6, "Metric"),
    (7, "Observation"),
    (8, "Opportunity"),
    (9, "Porblem"),
    (10, "Question"),
    (11, "Signal"),
    (12, "Test"),
)
SIGNAL_STATUS = (
    (0, "Opened"),
    (1, "Closed")
)

class Signal(MPTTModel):

    # Identify
    serial         = models.CharField(max_length=36, default=generate_serial, null=False, blank=False)
    icon           = models.CharField(default="bubble_chart", max_length=64)
    # Classify
    parent         = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')    
    classification = models.IntegerField(choices=SIGNAL_CLASSIFICATION, default=0, blank=False, null=False)
    status         = models.IntegerField(choices=SIGNAL_STATUS, default=0, blank=False, null=False)
    body           = models.TextField(max_length=512, blank=False, null=False)
    # Users
    circle         = models.ForeignKey("team.Circle", on_delete=models.CASCADE)
    owner          = models.ForeignKey("user.Account", on_delete=models.CASCADE, blank=False, null=False, related_name="owner")
    user           = models.ForeignKey("user.Account", on_delete=models.CASCADE, default=None, blank=True, null=True, related_name="user")
    # Time
    created        = models.DateTimeField(auto_now_add=True)
    updated        = models.DateTimeField(auto_now=True)
    #
    approved       = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.serial}"

    def url(self):
        return reverse("blog:signal", args=[str(self.serial)])
    
    def get_status_icon(self):
        if self.status == 0: return "line_start_circle"
        return "line_end_circle"
    
    def update_status(self):
        return reverse("blog:update_status", args=[str(self.serial)])