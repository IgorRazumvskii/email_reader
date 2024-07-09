from django.db import models


class EmailAccount(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)

    def __str__(self):
        return self.email


class Email(models.Model):
    account = models.ForeignKey(EmailAccount, on_delete=models.CASCADE, related_name='emails')
    subject = models.CharField(max_length=255)
    send_date = models.DateTimeField()
    received_date = models.DateTimeField()
    body = models.TextField()
    attachments = models.JSONField(default=list)

    def __str__(self):
        return self.subject
