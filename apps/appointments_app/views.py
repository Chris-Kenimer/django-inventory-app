from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.sessions.models import Session
import datetime
from .models import Appointment
from ..user_dashboard_app.models import User
# Create your views here.
def index(request):
    appointments_today = Appointment.objects.filter(date=datetime.date.today()).order_by('Time')
    future_appointments = Appointment.objects.filter(date__gt=datetime.date.today()).order_by('date')
    context = {
        'appointments_today': appointments_today,
        'future_appointments': future_appointments,
    }
    return render(request, 'appointments_app/appointments.html', context)
def add_appointment(request):
    if request.session.get('user'):
        user =  User.objects.get(id=request.session['user']['id'])
        appointment = Appointment.objects.validate_appointment_fields(request.POST)
        try:
            date_converted = datetime.datetime.strptime(request.POST['date'],"%m/%d/%Y").date()
        except ValueError:
            errors.append('Please enter valid date format mm/dd/yyyy')
        if appointment[0]:
            new_appointment = Appointment.objects.create(task_name=request.POST['task'], date=date_converted, Time=request.POST['time'], user=user, status='Pending')
            print new_appointment
        else:
            for error in appointment[1]:
                messages.warning(request, error)
            print appointment
    else:
        messages.warning(request, 'You must be logged in to add an appointment')
    return redirect('/appointments')
def edit_appointment( request, id):
        try:
            appointment = Appointment.objects.get(id=id)
            context = {
                'appointment': appointment,
            }
            return render(request, 'appointments_app/edit_appointment.html', context)
        except Appointment.DoesNotExist:
            messages.warning(request, 'Could not find this appointment')
            return redirect('/appointments')

def update_appointment(request):
    if request.session.get('user'):
        user =  User.objects.get(id=request.session['user']['id'])
        appointment = Appointment.objects.validate_appointment_fields(request.POST)
        try:
            date_converted = datetime.datetime.strptime(request.POST['date'],"%m/%d/%Y").date()
        except ValueError:
            messages.warning('Please enter valid date format mm/dd/yyyy')
        if appointment[0]:
            appointment_id = request.POST['appointment_id']
            update_appointment = Appointment.objects.filter(id=appointment_id).update(task_name=request.POST['task'], date=date_converted, Time=request.POST['time'], user=user, status=request.POST['status'])
            print update_appointment
        else:
            for error in appointment[1]:
                messages.warning(request, error)
            print appointment
    else:
        messages.warning(request, 'You must be logged in to add an appointment')
    return redirect('appointments/edit_appointment/'+request.POST['appointment_id'])
def remove_appointment(request, id):
    Appointment.objects.get(id=id).delete()
    return redirect('/appointments')
