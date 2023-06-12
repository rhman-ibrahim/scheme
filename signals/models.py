import uuid
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
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
        order_insertion_by=['-created']    


class Problem(Signal):
    
    def __str__(self):
        return f'Problem, posted by {self.author.username}'


class Opportunity(Signal):

    def __str__(self):
        return f'Opportunity, posted by {self.author.username}'
    
    class Meta:
        verbose_name_plural = "Opportunities"


class Hypothesis(Signal):

    content_type   = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id      = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    
    def __str__(self):
        return f'Hypothesis, posted by {self.user.username}'


class SignalThread(Signal):

    connector = models.ForeignKey("signals.Hypothesis", on_delete=models.CASCADE)
    

# Observation, Insight, Decisions
class LearningThread(SignalThread):

    type = models.IntegerField(choices=LEARNING_THREAD_SIGNAL_TYPES, blank=True, null=True)
    
    def __str__(self):
        return f'{ self.type } by {self.user.username}'
    
    def pre_save(self, *args, **kwargs):
        self.type = self.level
        super().pre_save(*args, **kwargs)


# Test, Metric, Criteria
class TestingThread(SignalThread):

    type = models.IntegerField(choices=TEST_THREAD_SIGNAL_TYPES, blank=True, null=True)
    
    def __str__(self):
        return f'{ self.type } by {self.user.username}'
    
    def pre_save(self, *args, **kwargs):
        self.type = self.level
        super().pre_save(*args, **kwargs)