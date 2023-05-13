import re
import uuid

from django.urls import reverse
from django.db import models

from mptt.models import MPTTModel, TreeForeignKey


def structure(text):

    message  = str(text)
    hashtag  = '(#\w+)'
    hashtags = re.findall(hashtag, str(text)) if re.search(hashtag, text) else []
    
    if len(hashtags) > 0:

        anchors  = [f'<a href="#{word}">{word}</a>' for word in hashtags]
        index    = 0

        while index != len(hashtags):

            message = message.replace(hashtags[index], anchors[index])
            index  += 1
    
    return message


class Signal(MPTTModel):

    PRIVACY_CHOICES = (
        (0, "Only Me"),
        (1, "Connected"),
        (2, "Circle"),
        (3, "Followers")
    )

    STATUS_CHOICES = (
        (0, "Opened"),
        (1, "Closed")
    )

    GRADE_CHOICES = (
        (0, "Negative"),
        (1, "Netural"),
        (2, "Postive"),
    )

    EVALUATION_CHOICES = (
        (0, "All"),
        (1, "Latest"),
    )

    parent     = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    user       = models.ForeignKey("user.Account", on_delete=models.CASCADE, blank=False, null=False)
    user       = models.ForeignKey("circles.Circle", on_delete=models.SET_NULL, blank=True, null=True, default=None)

    serial     = models.UUIDField(default=uuid.uuid4, editable=False)
    message    = models.TextField(max_length=512, blank=False, null=False)

    privacy    = models.IntegerField(choices=PRIVACY_CHOICES, default=0, blank=False, null=False)
    status     = models.IntegerField(choices=STATUS_CHOICES, default=0, blank=False, null=False)
    grade      = models.IntegerField(choices=GRADE_CHOICES, default=1, blank=False, null=False)
    evaluation = models.IntegerField(choices=EVALUATION_CHOICES, default=1, blank=False, null=False)
    latest     = models.IntegerField(default=1, blank=False, null=False)

    created    = models.DateTimeField(auto_now_add=True)
    updated    = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'by {self.user.username}'

    def print(self):
        return structure(self.message)

    def tree(self):
        if self.level == 1:
            return [self.parent, self]
        elif self.level == 2:
            return [self.get_root(), self.parent, self]
        elif self.level == 3:
            return [self.get_root(), self.parent.parent, self.parent, self]

    @property
    def privacy_state(self):
        if self.is_root_node():
            return "lock" if self.privacy == 0 else "public"
        else:
            return self.get_root().privacy_state
    
    @property
    def status_state(self):
        if self.level != 3:
            return "line_start_circle" if self.status == 0 else "line_end_circle"
        else:
            if not self.get_next_sibling():
                return "line_end_circle"
            elif not self.get_previous_sibling():
                return "line_start_circle"
            else:
                return "commit"

    class MPTTMeta:
        order_insertion_by=['-created']



class Comment(MPTTModel):

    user       = models.ForeignKey("user.Account", on_delete=models.CASCADE, blank=False, null=False)
    signal     = models.ForeignKey("signals.Signal", on_delete=models.CASCADE, blank=False, null=False)
    parent     = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    serial     = models.UUIDField(default=uuid.uuid4, editable=False)
    message    = models.TextField(max_length=512, blank=False, null=False)

    created    = models.DateTimeField(auto_now_add=True)
    updated    = models.DateTimeField(auto_now=True)


class Note(MPTTModel):


    signal  = models.ForeignKey("signals.Signal", on_delete=models.CASCADE, blank=False, null=False)
    user    = models.ForeignKey("user.Account", on_delete=models.CASCADE, blank=False, null=False)
    parent  = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    serial  = models.UUIDField(default=uuid.uuid4, editable=False)    
    message = models.TextField(max_length=512, blank=False, null=False)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'by {self.user.username}'
    
    def print(self):
        return structure(self.message)

    def view(self):
        return reverse("signals:read_comment", args=[str(self.id)])
        
    def delete(self):
        return reverse("signals:delete_comment", args=[str(self.id)])