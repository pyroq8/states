from django.shortcuts import render, render_to_response
from django.http import HttpResponse

from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

from django.template import RequestContext
from main.forms import CitySearch, CreateCity
# Create your views here.
from main.models import State, City, StateCapital

from django.contrib.auth.models import User
from main.forms import UserSignUp
from django.db import IntegrityError
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseRedirect

def home(request):

	context = {}

	states = State.objects.all()
	context['states'] = states

	return render_to_response("home.html", context, context_instance=RequestContext(request))


def city_detail(request, pk):

	context = {}

	city = City.objects.get(pk=pk)

	context['city'] = city

	return render_to_response('city_detail.html', context, context_instance=RequestContext(request))
	

def first_view(request):

	states = State.objects.all()

	state_list = ""
	
	for state in states:
		for city in state.city_set.all():
			state_list += "State: %s, City %s, zip %s</br>" %(state.name, city.name, city.zip_code)

	return HttpResponse(state_list)


def city_search(request, city, state):

	states = State.objects.filter(name__istartswith=state)

	city_string = ""

	for state in states:
		cities = state.city_set.filter(name__istartswith=city)
		for city in cities:
			city_string += "State:%s , City:%s</br>" % (state.name, city.name)

	return HttpResponse(city_string)



def get_view(request):

	get_var1 = request.GET.get('var1', None)
	get_var2 = request.GET.get('var2', None)
	get_var3 = request.GET.get('var3', None)

	request = "<pre> %s </pre>" % request

	return HttpResponse(request)

def get_city_state(request):

	state = request.GET.get('state', None)
	city = request.GET.get('city', None)

	#city_state = "%s , %s" % (city, state)
	city_state = """
	<form action='/get_city_state' method='GET'>

	State:
	</br>
	<input type="text" name="state" >

	</br>

	City:
	</br>
	<input type="text" name="city" >

	</br>

	<input type="submit" value="Submit Me">
	
	</form>
	</br>
	</br>
	"""

	if state != None and city != None:
		states = State.objects.filter(name__istartswith=state)

		for state in states:
			cities = state.city_set.filter(name__istartswith=city)
			for city in cities:
				city_state+= "%s , %s, </br>" % (city.name, state.name)


	return HttpResponse(city_state)

@csrf_exempt
def post_city_state(request):

	city_state = """
		<form action='/post_city_state/' method='POST'>

		State:
		</br>
		<input type="text" name="state" >

		</br>

		City:
		</br>
		<input type="text" name="city" >

		</br>

		<input type="submit" value="Submit Me">
	
		</form>
		</br>
		</br>
	"""

	if request.method == 'GET':

		return HttpResponse(city_state)

	if request.method == 'POST':

		state = request.POST.get('state', None)
		city = request.POST.get('city', None)

	
		if state != None and city != None:
			states = State.objects.filter(name__istartswith=state)

			for state in states:
				cities = state.city_set.filter(name__istartswith=city)
				for city in cities:
					city_state+= "%s , %s, %s, %s, %s</br>" % (city.name, state.name, state.abbreviation, city.latitude, city.longitude)


		return HttpResponse(city_state)

class GetPost(View):

	def get(self, request, *args, **kwargs):
		get_string = "This is a Get String"

		return HttpResponse(get_string)

	def post(self, request, *args, **kwargs):
		post_string = "This is a Post String"

		return HttpResponse(post_string)


def template_view(request):

	states = State.objects.filter(name__contains="A")
	
	context = {}

	context['states'] = states

	return render(request, 'city_list.html', context)


def template_view2(request):

	states = State.objects.all()

	context = {}

	state_city = {}
	
	for state in states:
		
		cities = state.city_set.filter(name__contains="A")

		state.name = { state.name : cities }

		state_city.update(state.name)

	print state_city

	context['state_city'] = state_city

	#return render(request, 'base2.html', context)

	return render_to_response('base2.html', context, context_instance=RequestContext(request))



def form_view(request):

	context = {}

	get = request.GET
	post = request.POST

	context['get'] = get
	context['post'] = post


	if request.method == "POST":
		city = request.POST.get('city', None)

		cities = City.objects.filter(name__startswith=city)

		context['cities'] = cities

	elif request.method == "GET":
		context['method'] = 'The method was GET'

	return render_to_response('form_view.html', context, context_instance=RequestContext(request))


def form_view2(request):

	context = {}

	get = request.GET
	post = request.POST

	context['get'] = get
	context['post'] = post

	form = CitySearch()
	context['form'] = form


	if request.method == "POST":
		form = CitySearch(request.POST)

		if form.is_valid():
			city = form.cleaned_data['name']

			cities = City.objects.filter(name__startswith=city)

			context['cities'] = cities
			context['valid'] = "The Form was Valid"

		else:
			context['valid'] = form.errors


	elif request.method == "GET":
		context['method'] = 'The method was GET'

	return render_to_response('form_view2.html', context, context_instance=RequestContext(request))


def city_create(request):

	context = {}

	form = CreateCity()
	context['form'] = form

	if request.method == 'POST':
		form = CreateCity(request.POST)

		if form.is_valid():
			form.save()

			context['valid'] = "City Saved"

	elif request.method == 'GET':
		context['valid'] = form.errors

	return render_to_response('city_create.html', context, context_instance=RequestContext(request))



def signup(request):

	context = {}

	form = UserSignUp()
	context['form'] = form

	if request.method == 'POST':
		form = UserSignUp(request.POST)
		if form.is_valid():

			name = form.cleaned_data['name']
			email = form.cleaned_data['email']
			password = form.cleaned_data['password']

			try:
				new_user = User.objects.create_user(name, email, password)
				context['valid'] = "Thank You For Signing Up!"

				auth_user = authenticate(username=name, password=password)
				login(request, auth_user)
				return HttpResponseRedirect('/template_view/')

			except IntegrityError, e:
				context['valid'] = "A User With That Name Already Exists"

			#User.objects.create_user(name, email, password)

		else:
			context['valid'] = form.errors

	if request.method == 'GET' :
		context['valid'] = "Please Sign Up!!"


	return render_to_response('signup.html', context, context_instance=RequestContext(request))

















