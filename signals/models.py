import uuid
from django.db import models
# from django.contrib.contenttypes.fields import GenericForeignKey
# from django.contrib.contenttypes.models import ContentType
from mptt.models import MPTTModel, TreeForeignKey


LEARNING_THREAD_SIGNAL_TYPES = (
    (0, "Observation"),
    (1, "Insight"),
    (2, "Decision")
)
TEST_THREAD_SIGNAL_TYPES = (
    (0, "Test"),
    (1, "Metric"),
    (2, "Criteria")
)



class Signal(MPTTModel):

    serial      = models.UUIDField(default=uuid.uuid4, editable=False)
    parent      = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')    
    body        = models.TextField(max_length=512, blank=False, null=False)
    # Users
    author      = models.ForeignKey("user.Account", on_delete=models.CASCADE, blank=False, null=False, related_name="author")
    contributor = models.ForeignKey("user.Account", on_delete=models.CASCADE, default=None, blank=True, null=True, related_name="contributor")
    circle      = models.ForeignKey("circles.Circle", on_delete=models.CASCADE)
    # Time
    created     = models.DateTimeField(auto_now_add=True)
    updated     = models.DateTimeField(auto_now=True)
    #
    approved    = models.BooleanField(default=False)

    class MPTTMeta:
        abstract = True
    
    def get_icon(self):

        if isinstance(self, Problem):
            return self.problem.icon
        
        if isinstance(self, Opportunity):
            return self.opportunity.icon


class Problem(Signal):
    
    icon = models.CharField(default="psychology_alt", editable=False, max_length=64)

    def __str__(self):
        return f'Problem, posted by {self.author.username}'


class Opportunity(Signal):

    icon = models.CharField(default="psychology", editable=False, max_length=64)

    def __str__(self):
        return f'Opportunity, posted by {self.author.username}'
    
    class Meta:
        verbose_name_plural = "Opportunities"