from django.db import models


class Contact(models.Model):
    """
    Contact form field models
    """
    name = models.CharField(max_length=100, blank=False, null=False)
    email = models.EmailField(blank=False, null=False)
    subject = models.CharField(max_length=100, blank=False, null=False)
    message = models.TextField(blank=False, null=False)

    def __str__(self):
        return self.email
