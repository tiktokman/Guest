from django.contrib import auth as django_auth
import base64
import time, hashlib

def user_auth(request):
	get_http_auth =  request.META.get('HTTP_AUTHORIZATION', b'')
	auth = get_http_auth.split()
	try:
		auth_parts = base64.b64decode(auth[1]).decode('utf-8').partition(':')
	except IndexError:
		return 'null'
	username, password = auth_parts[0]. auth_parts[2]
	user = django_auth.atuhenticate(username = username, password = password)

	if user is not None:
		django_auth.login(request, user)
		return 'success'
	else:
		return 'fail'


def user_sign(request):
	if request.method == 'POST':
		client_time = request.POST.get('time', '')
		client_sign = request.POST.get('sign', '')
	else:
		return 'error'

	if client_time == '' or client_sign == '':
		return 'sign null'

	now_time = time.time()
	server_time = str(now_time).split('.')[0]

	time_difference = int(server_time) - int(client_time)
	if time_difference >= 60 :
		return 'timeout'

	md5 = hashlib.md5()
	sign_str = client_time + '&Guest-Bugmaster'
	sign_bytes_utf8 = sign_str.encode(encoding = 'utf-8')
	md5.update(sign_bytes_utf8)
	server_sign = md5.hexdigest()

	if server_sign != client_sign :
		return 'sign fail'
	else:
		return 'sign success'
