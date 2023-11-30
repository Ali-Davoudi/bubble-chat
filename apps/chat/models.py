from django.db import models

from apps.account.models import User


class Message(models.Model):
    body = models.TextField()
    sent_by = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.sent_by

    class Meta:
        ordering = ('created_by',)
        db_table = 'user_message'


class Room(models.Model):
    WAITING = 'waiting'
    ACTIVE = 'active'
    CLOSED = 'closed'

    CHOICES_STATUS = (
        (WAITING, 'Waiting'),
        (ACTIVE, 'Active'),
        (CLOSED, 'Closed')
    )

    uuid = models.CharField(max_length=255)
    client = models.CharField(max_length=200)
    agent = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='rooms', null=True, blank=True)
    messages = models.ManyToManyField(Message, blank=True)
    url = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=100, choices=CHOICES_STATUS, default=WAITING)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.client} - {self.uuid}'

    class Meta:
        ordering = ('-created_at',)
        db_table = 'room'
