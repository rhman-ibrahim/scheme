# Django
from django.db import models
from django.urls import reverse
from django.utils.crypto import get_random_string
# MPTT
from mptt.models import MPTTModel, TreeForeignKey


SIGNAL_CLASSIFICATION   = (
    (0, "Problem"),
    (1, "Opportunity"),
    (2, "Hypothesis"),

    (3, "Observation"),
    (4, "Insight"),
    (5, "Decision"),
    
    (6, "Test"),
    (7, "Metric"),
    (8, "Criteria")
)
SIGNAL_STATUS = (
    (0, "Opened"),
    (1, "Closed")
)


class Signal(MPTTModel):

    # Identify
    serial         = models.CharField(max_length=36, default=get_random_string(length=32), null=False, blank=False)
    icon           = models.CharField(default="bubble_chart", max_length=64)
    # Classify
    parent         = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')    
    classification = models.IntegerField(choices=SIGNAL_CLASSIFICATION, default=0, blank=False, null=False)
    status         = models.IntegerField(choices=SIGNAL_STATUS, default=0, blank=False, null=False)
    body           = models.TextField(max_length=512, blank=False, null=False)
    # Users
    circle         = models.ForeignKey("circles.Circle", on_delete=models.CASCADE)
    owner          = models.ForeignKey("user.Account", on_delete=models.CASCADE, blank=False, null=False, related_name="owner")
    user           = models.ForeignKey("user.Account", on_delete=models.CASCADE, default=None, blank=True, null=True, related_name="user")
    # Time
    created        = models.DateTimeField(auto_now_add=True)
    updated        = models.DateTimeField(auto_now=True)
    #
    approved       = models.BooleanField(default=False)

    def url(self):
        return reverse("signals:signal", args=[str(self.serial)])
    
    def get_status_icon(self):
        if self.status == 0: return "line_start_circle"
        return "line_end_circle"
    
    def update_status(self):
        return reverse("signals:update_status", args=[str(self.serial)])