from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from sign.models import Event, Guest
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
def index(request):
	return render(request, 'index.html')

def login_action(request):
	if request.method == 'POST':
		username = request.POST.get('username', '')
		password = request.POST.get('password', '')

		user = auth.authenticate(username = username, password = password)

		if user is not None:
			auth.login(request, user)
			response =  HttpResponseRedirect('/event_manage/')
			request.session['user'] = username
			return response
		else:
			return render(request, 'index.html', {'error':'username or password error'})

@login_required
def event_manage(request):
	event_list = Event.objects.all()
	username = request.session.get('user', '')
	return render(request, 'event_manage.html', {'user':username, 'events':event_list})

@login_required
def guest_manage(request):
	username = request.session.get('user', '')
	guests_list = Guest.objects.all()
	paginator = Paginator(guests_list, 2)
	page = request.GET.get('page')
	try:
		contacts = paginator.page(page)
	except PageNotAnInteger:
		contacts = paginator.page(1)
	except EmptyPage:
		contacts = paginator.page(paginator.num_pages)

	return render(request, 'guest_manage.html', {'user':username, 'guests':contacts})

	
@login_required
def search_event(request):
	username = request.session.get('user', '')
	search_name = request.GET.get('name', '')
	event_list = Event.objects.filter(name__contains = search_name)
	return render(request, 'event_manage.html', {'user':username, 'events':event_list})

	
@login_required
def search_guest(request):
	username = request.session.get('user', '')
	search_name = request.GET.get('name', '')
	guests_list = Guest.objects.filter(realname__contains = search_name)
	paginator = Paginator(guests_list, 2)
	page = request.GET.get('page')
	try:
		contacts = paginator.page(page)
	except PageNotAnInteger:
		contacts = paginator.page(1)
	except EmptyPage:
		contacts = paginator.page(paginator.num_pages)

	return render(request, 'guest_manage.html', {'user':username, 'guests':contacts})

@login_required
def logout(request):
	auth.logout(request)
	response =  HttpResponseRedirect('/index/')
	return response

@login_required
def sign_index(request, eid):
	event = get_object_or_404(Event, id = eid)
	guestnum = Guest.objects.all().count()
	guestsigned = Guest.objects.filter(sign='1').count()

	return render(request, 'sign_index.html', {'event':event,
											   'guestnum':guestnum,
											   'guestsigned':guestsigned,
														})

@login_required
def sign_index_action(request, eid):
	event = get_object_or_404(Event, id = eid)
	phone = request.POST.get('phone', '')
	result = Guest.objects.filter(phone = phone)
	guestnum = Guest.objects.all().count()
	guestsigned = Guest.objects.filter(sign='1').count()

	if not result:
		return render(request, 'sign_index.html', {'event':event,
												   'hint':'phone error',
												    'guestnum':guestnum,
											   		'guestsigned':guestsigned,
															})
	result = Guest.objects.filter(phone = phone, event_id = eid)

	if not result:
		return render(request, 'sign_index.html', {'event':event,
												   'hint':'eventid or phone error',
												    'guestnum':guestnum,
											  		'guestsigned':guestsigned,
															})

	result = Guest.objects.get(phone = phone, event_id = eid)
	if result.sign:
		return render(request, 'sign_index.html', {'event':event,
												   'hint':'user already sign in',
												   'guestnum':guestnum,
											   	   'guestsigned':guestsigned,
															})
	else:
		Guest.objects.filter(phone = phone, event_id = eid).update(sign='1')
		guestnum = Guest.objects.all().count()
		guestsigned = Guest.objects.filter(sign='1').count()
		return render(request, 'sign_index.html', {'event':event,
												   'hint':'sign in success',
												   'guest':result,
												   'guestnum':guestnum,
											   	   'guestsigned':guestsigned,
															})

