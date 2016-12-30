from __future__ import unicode_literals

from django.db import models
import datetime
import re
# Create your models here.
class QuoteManager(models.Manager):
    def validate_quote_fields(self, data):
        errors = []

        if len(data['quoted_by']) < 4:
            errors.append('Please enter a valid name - 4 character minimum')
        if not re.search(r'^[ a-zA-Z.+_-]+$', data['quoted_by']):
            errors.append('Please enter a valid name, no special characters or numbers')
        if len(data['message']) < 11:
            errors.append('Please enter worthy quote - Greater than 10 characters')
        if len(data['message']) > 500:
            errors.append('Please limit the quote to 500 characters')
        if not errors:
            errors.append('New Quote entered')
            return (True, errors)
        else:
            return (False, errors)

class Quote(models.Model):
    quoted_by = models.CharField(max_length=45, blank=True, null=True)
    message = models.CharField(max_length=500, blank=True, null=True)
    user = models.ForeignKey('user_dashboard_app.User')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = QuoteManager()

    class Meta:
        managed = True
        db_table = 'quotes'
class Favorite(models.Model):
    user = models.ForeignKey('user_dashboard_app.User')
    quote = models.ForeignKey(Quote)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'favorites'
