from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.sessions.models import Session
import datetime
from .models import Quote, Favorite
from ..user_dashboard_app.models import User
# Create your views here.
def index(request):
    if request.session.get('user'):
        user =  User.objects.get(id=request.session['user']['id'])
        quotes = Quote.objects.exclude(favorite__user=user)
        favorites = Favorite.objects.filter(user=user)
        for favorite in favorites:
            print favorite.quote.quoted_by
        context = {
            'quotes': quotes,
            'favorites': favorites,
        }
        return render(request, 'quotes_app/index.html', context)
    else:
        return render(request, 'quotes_app/index.html')
def add_quote(request):
    if request.POST:
        print request.POST['quoted_by']
        print request.POST['message']
        user =  User.objects.get(id=request.session['user']['id'])
        validate_quote = Quote.objects.validate_quote_fields(request.POST)
        if validate_quote[0]:
            new_quote = Quote.objects.create(quoted_by=request.POST['quoted_by'], message=request.POST['message'], user=user)
            print new_quote
        else:
            for error in validate_quote[1]:
                messages.warning(request, error)
    return redirect('/quotes')
def favorite_a_quote(request):
    if request.session.get('user'):
        user =  User.objects.get(id=request.session['user']['id'])
        id = request.POST['quote_id']
        try:
            quote = Quote.objects.get(id=id)
            valid_quote = True

        except Quote.DoesNotExist:
            messages.warning(request, 'Could not find this quote')
            valid_quote = False
            return redirect('/quotes')

        if valid_quote:
            new_favorite = Favorite.objects.create(user=user, quote=quote)
            return redirect('/quotes')
def remove_favorite(request):
    if request.session.get('user'):
        user =  User.objects.get(id=request.session['user']['id'])
        id = request.POST['favorite_id']
        try:
            favorite = Favorite.objects.get(id=id)
            valid_favorite = True

        except Quote.DoesNotExist:
            messages.warning(request, 'Could not find this quote')
            valid_favorite = False
            return redirect('/quotes')

        if valid_favorite:
            if favorite.user.id == user.id:
                print 'This user owns this favorite'
                favorite.delete()
            return redirect('/quotes')
