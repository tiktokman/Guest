from django.test import TestCase
from sign.models import Event, Guest
from django.contrib.auth.models import User

# Create your tests here.

class ModelTest(TestCase):

	def setUp(self):
		Event.objects.create(
							 id = 1,
							 name = "oneplus 3 event",
							 status = True,
							 limit = 2000,
							 address = 'shenzhen',
							 start_time = '2016-08-31 02:18:22'
							)


		Guest.objects.create(
							 id = 1,
							 event_id = 1,
							 realname = 'alen',
							 phone = '13711001101',
							 email = 'alen@mail.com',
							 sign = False
							)

	def test_event_models(self):
		result = Event.objects.get(name = 'oneplus 3 event')
		self.assertEqual(result.address, 'shenzhen')
		self.assertTrue(result.status)

	def test_guest_models(self):
		result = Guest.objects.get(phone = '13711001101')
		self.assertEqual(result.realname, 'alen')
		self.assertFalse(result.sign)

class IndexPageTest(TestCase):

	def test_index_page_renders_index_template(self):
		response = self.client.get('/index/')
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'index.html')

class LoginActionTest(TestCase):

	def setUp(self):
		User.objects.create_user('admin', 'admin@mail.com', 'admin123456')

	def test_add_admin(self):
		user = User.objects.get(username = 'admin')
		self.assertEqual(user.username, 'admin')
		self.assertEqual(user.email, 'admin@mail.com')

	def test_login_action_username_password_null(self):
		test_data = {'username':'','password':''}
		response = self.client.post('/login_action/', data = test_data)
		self.assertEqual(response.status_code, 200)
		self.assertIn(b'username or password error', response.content)

	def test_login_action_username_password_error(self):
		test_data = {'username':'abc','password':'123'}
		response = self.client.post('/login_action/', data = test_data)
		self.assertEqual(response.status_code, 200)
		self.assertIn(b'username or password error', response.content)

	def test_login_action_success(self):
		test_data = {'username':'admin','password':'admin123456'}
		response = self.client.post('/login_action/', data = test_data)
		self.assertEqual(response.status_code, 302)


class EventManageTest(TestCase):

	def setUp(self):
		User.objects.create_user('admin', 'admin@mail.com', 'admin123456')
		Event.objects.create(
							 id = 1,
							 name = "oneplus 3 event",
							 status = True,
							 limit = 2000,
							 address = 'shenzhen',
							 start_time = '2016-08-31 02:18:22'
							)		
		self.login_user_data = {'username':'admin', 'password':'admin123456'}

	def test_event_manage_success(self):
		response = self.client.post('/login_action/', data = self.login_user_data)
		response = self.client.post('/event_manage/')
		self.assertEqual(response.status_code, 200)
		self.assertIn(b'oneplus', response.content)
		self.assertIn(b'shenzhen', response.content)

	def test_event_manage_search_success(self):
		response = self.client.post('/login_action/', data = self.login_user_data)
		response = self.client.post('/search_event/', data= {'name':'oneplus'})
		self.assertIn(b'oneplus', response.content)
		self.assertIn(b'shenzhen', response.content)

class GuestManageTest(TestCase):

	def setUp(self):
		User.objects.create_user('admin', 'admin@mail.com', 'admin123456')
		Event.objects.create(
							 id = 1,
							 name = "oneplus 3 event",
							 status = True,
							 limit = 2000,
							 address = 'shenzhen',
							 start_time = '2016-08-31 02:18:22'
							)	
		Guest.objects.create(
							 id = 1,
							 event_id = 1,
							 realname = 'alen',
							 phone = '13711001101',
							 email = 'alen@mail.com',
							 sign = False
							)
		self.login_user_data = {'username':'admin', 'password':'admin123456'}

	def test_guest_manage_success(self):
		response = self.client.post('/login_action/', data = self.login_user_data)
		response = self.client.post('/guest_manage/')
		self.assertEqual(response.status_code, 200)
		self.assertIn(b'alen', response.content)
		self.assertIn(b'13711001101', response.content)

	def test_guest_manage_search_success(self):
		response = self.client.post('/login_action/', data = self.login_user_data)
		response = self.client.post('/search_guest/', data= {'name':'alen'})
		self.assertIn(b'alen', response.content)
		self.assertIn(b'13711001101', response.content)

class SignIndexActionTest(TestCase):
	
	def setUp(self):
		User.objects.create_user('admin', 'admin@mail.com', 'admin123456')
		Event.objects.create(
							 id = 1,
							 name = "oneplus 3 event",
							 status = True,
							 limit = 2000,
							 address = 'shenzhen',
							 start_time = '2016-08-31 02:18:22'
							)	
		Event.objects.create(
							 id = 2,
							 name = "meizu5 event",
							 status = True,
							 limit = 2000,
							 address = 'beijing',
							 start_time = '2016-08-01 02:18:22'
							)	
		Guest.objects.create(
							 id = 1,
							 event_id = 1,
							 realname = 'alen',
							 phone = '13711001101',
							 email = 'alen@mail.com',
							 sign = 0
							)
		Guest.objects.create(
							 id = 2,
							 event_id = 2,
							 realname = 'leeca',
							 phone = '15692005742',
							 email = 'leeca@mail.com',
							 sign = 1
							)
		self.login_user_data = {'username':'admin', 'password':'admin123456'}		

	def test_sign_index_action_phone_null(self):
		response = self.client.post('/login_action/', data = self.login_user_data)
		response = self.client.post('/sign_index_action/1/', {'phone':''})
		self.assertEqual(response.status_code, 200)
		self.assertIn(b'phone error', response.content)

	def test_sign_index_action_phone_or_eventid_error(self):
		response = self.client.post('/login_action/', data = self.login_user_data)
		response = self.client.post('/sign_index_action/2/', {'phone':'15692005744'})
		self.assertEqual(response.status_code, 200)
		self.assertIn(b'error', response.content)

	def test_sign_already(self):
		response = self.client.post('/login_action/', data = self.login_user_data)
		response = self.client.post('/sign_index_action/2/', {'phone':'15692005742'})
		self.assertEqual(response.status_code, 200)
		self.assertIn(b'already', response.content)

	def test_sign_success(self):
		response = self.client.post('/login_action/', data = self.login_user_data)
		response = self.client.post('/sign_index_action/1/', {'phone':'13711001101'})
		self.assertEqual(response.status_code, 200)
		self.assertIn(b'success', response.content)
