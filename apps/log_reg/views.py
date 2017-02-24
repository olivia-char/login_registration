from django.shortcuts import render, redirect, HttpResponse
from .models import User
from django.contrib import messages

# Create your views here.

def index(request):
	print "first page"
	if 'id' not in request.session:
		request.session['id'] = 0

	return render(request, 'log_reg/index.html')

def register(request):
	print "register page"
	if request.method == 'POST':
		fname = request.POST['first_name']
		lname = request.POST['last_name']
		email = request.POST['email']
		pw = request.POST['password']
		cpw = request.POST['c_password']

	newUser = User.userManager.register(fname, lname, email, pw, cpw)
	if newUser[0] == False:
		print newUser[1]['errorMessage']
		errorMessage = newUser[1]['errorMessage']
		print errorMessage
		for i in errorMessage:
			messages.error(request, i)
			print i
		return redirect('/')
	else:
		messages.info(request, "Welcome " + fname)
		messages.success(request, "successfully registered")		
		return redirect("/success")

def login(request):
	print "login page"
	if request.method == 'POST':
		email = request.POST['email']
		password = request.POST['password']

	login = User.userManager.login(email, password)
	if login[0] == False:
		errorMessage = login[1]['errorMessage']
		for i in errorMessage:
			messages.error(request, i)
		return redirect('/') 
	else:
		messages.info(request, "Welcome Back!")
		return redirect('/success') 


def success(request):
	if 'id' not in request.session or request.session['id'] == 0:
		return redirect('/')
	print "success!"
	return render(request, 'log_reg/success.html')