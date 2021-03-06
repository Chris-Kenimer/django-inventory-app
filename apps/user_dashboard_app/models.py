from __future__ import unicode_literals

from django.db import models
import datetime
import re, bcrypt
#
# from ..auth_app.models import User
# Create your models here.
class UserManager(models.Manager):
    def validate_user_fields(self, data):
        errors = []
        try:
            date_converted = datetime.datetime.strptime(data['date_of_birth'],"%m/%d/%Y").date()
        except ValueError:
            errors.append(['date_of_birth', 'Please enter valid date format mm/dd/yyyy'])
        if len(data['first_name']) < 2:
            errors.append(['first_name', 'Please enter a valid first name'])
        elif not re.search(r'^[a-zA-Z\s-]+$',data['first_name']):
            errors.append(['first_name', 'First name must only contain letters'])
        if len(data['last_name']) < 2:
            errors.append(['last_name', 'Please enter a valid last name'])
        elif not re.search(r'^[a-zA-Z\s-]+$',data['last_name']):
            errors.append(['first_name', 'Last name must only contain letters'])
        if not re.search(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$', data['email']):
            errors.append(['email','Please enter a valid email address'])
        if User.objects.filter(email=data['email']):
            errors.append(['email', 'This email already exists in the system, try to login'])
        if not data['password'] == data['confirm_password']:
            errors.append(['password_match_error', 'Password fields do not match'])
        elif not re.search(r'^(?=.*[a-z])(?=.*\d)(?=.*[A-Z])(?:.{8,})$', data['password']):
            errors.append(['length_complexity', 'Requirements: 8 Characters, Capital letters, and numbers'])
        if not errors:
            return (True, errors)
        else:
            return (False, errors)
    def login(self, data):
        errors = []
        user = User.objects.filter(email=data['email'])
        if user:
            if not User.objects.validate_password(data['password'], user):
                errors.append('Incorrect password')
                print 'Incorrect'
        else:
            errors.append('Could not find a user in the system')
            print 'could not find a user'
        if not errors:
            return (True, user[0])
        else:
            return (False, errors)
    def validate_password(self, password, user):
        if not bcrypt.hashpw(password.encode(),user[0].password.encode()) == user[0].password:
            return False
        return True
    def check_if_admin(self, user):
        return True
    def delete_all(self):
        User.objects.all().delete()

class User(models.Model):
    first_name = models.CharField(max_length=45, blank=True, null=True)
    last_name = models.CharField(max_length=45, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    email = models.CharField(max_length=60, blank=True, null=True)
    password = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

    class Meta:
        managed = True
        db_table = 'users'
