from __future__ import unicode_literals
from django.db import models
import re 
import bcrypt

NAME_REGEX = re.compile(r'^[a-zA-Z]+$')
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# Create your models here.

class UserManager(models.Manager):
	def register(self, first_name, last_name, email, password, c_password):
		
		status = True 
		error = []

		if len(first_name) < 1:
			error.append("First Name Required")
			status = False
		elif len(first_name) <= 2:
			error.append("First Name must be more than 2 characters")
			status = False
		elif not NAME_REGEX.match(first_name):
			error.append("First Name cannot contain numbers")
			status = False
		
		if len(last_name) < 1:
			error.append("Last Name Required")
			status = False
		elif len(last_name) <= 2:
			error.append("Last Name must be more than 2 characters")
			status = False
		elif not NAME_REGEX.match(last_name):
			error.append("Last name cannot contain numbers")
			status = False
		
		if len(email) < 1:
			error.append("Email Required")
			status = False
		elif not EMAIL_REGEX.match(email):
			error.append("Enter a vaild email")
			status = False
		elif len(User.userManager.filter(email=email)) > 0:
			error.append("Email already taken")
			status = False
	
		if len(password) < 1:
			error.append("Password Required")
			status = False
		elif len(password) < 8:
			error.append("Password must be longer than 8 characters")
			status = False
		if password != c_password:
			error.append("Passwords do not match")
			status = False
		
		if status == False:
			return (False, {'errorMessage': error}) 
		if status == True:
			pwHash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
			print "hashed out"
			return (True, self.create(first_name=first_name, last_name=last_name, email=email, password=password))

	def login(self, email, password):
		
		status = True 
		error = []
		print "email delivered from views", email
		email = User.userManager.filter(email=email)
		password = User.userManager.filter(password=password)
		print email, password 
		
		if len(email[0].email) < 1:
			error.append("Email Required")
			status = False

		if len(password[0].password) < 1:
			error.append("Password Required")
			status = False

		if status == False:
			return (False, {'errorMessage': error})
		if status == True:
			return (True, {})


class User(models.Model):
	first_name = models.CharField(max_length = 45)
	last_name = models.CharField(max_length = 45)
	email = models.EmailField(max_length = 100)
	password = models.CharField(max_length = 100)
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	userManager = UserManager()