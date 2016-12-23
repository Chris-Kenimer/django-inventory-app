from __future__ import unicode_literals

from django.db import models
import datetime
import re
# Create your models here.
class AppointmentManager(models.Manager):
    def validate_appointment_fields(self, data):
        errors = []
        date_seleted = data['date']
        time = data['time']
        task = data['task']
        try:
            date_converted = datetime.datetime.strptime(date_seleted,"%m/%d/%Y").date()
        except ValueError:
            errors.append('Please enter valid date format mm/dd/yyyy')
        # print datetime.date.today()
        # print date_converted
        if not re.search(r'^[0-9]{2}/[0-9]{2}/[0-9]{4}', date_seleted):
            errors.append('Please enter a valid date. Use the date picker for assistance')
        elif datetime.date.today() > date_converted :
             errors.append('Please enter a date from Today onward')
        if not re.search(r'^[0-9]{2}:[0-9]{2}', time):
            errors.append('Please enter a valid time. Use the time picker for assistance')
        if len(task) < 1:
            errors.append('Please enter a valid task name')
        if not errors:
            errors.append('New appointment entered')
            return (True, errors)
        else:
            return (False, errors)

class Appointment(models.Model):
    task_name = models.CharField(max_length=45, blank=True, null=True)
    status = models.CharField(max_length=45, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    Time = models.TimeField(blank=True, null=True)
    user = models.ForeignKey('user_dashboard_app.User')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = AppointmentManager()

    class Meta:
        managed = True
        db_table = 'appointments'
