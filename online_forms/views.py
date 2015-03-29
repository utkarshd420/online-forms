from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate,logout
from django.contrib.auth import login as login_user
from django.contrib import staticfiles
import datetime, hashlib, json,os, random
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse

from models import *
# Create your views here.

@csrf_exempt
def login(request):
	if request.method == 'GET':
		return render_to_response('login.html')
	else:
		if request.user.is_authenticated():
			logout(request)
		user_name = request.POST.get('email')
		user_pass = request.POST.get('password')
		#user = user_table.objects.get( user_table__username = user_name,user_table__password = user_pass )
		user = authenticate(username = user_name,password = user_pass)
		print "hurray 1"
		if user is not None:
			print "hurray 1.1"
			if user.is_active:
				print "hurray 1.1.1"
				login_user(request,user)
				return HttpResponseRedirect('../../admin/')
			else:
				print "hurray 1.1.2"
				return render_to_response('login.html',{'errormsg':'User not active'})
		else:
			return render_to_response('login.html',{'errormsg':'Invalid login'})

@csrf_exempt
def signup(request):
	if request.method == 'GET':
		return render_to_response('signup.html')
	else:
		if request.user.is_authenticated():
			logout(request)
		user_email = request.POST.get('email')
		user_pass = request.POST.get('password')
		user_firstname = request.POST.get('firstname')
		user_lastname = request.POST.get('lastname')
		print 'hakunamana 1'
		user_list = User.objects.filter(username = user_email)
		print user_list
		if len(user_list) !=0 :
			print 'hakunamana 1.4'
			return render_to_response('signup.html',{'errormsg':'User already registered!!'})
		else:
			print 'hakunamana 1.8'
			user = User.objects.create_user(username=user_email,password=user_pass,email=user_email,first_name=user_firstname,last_name=user_lastname)
			user.is_staff = True
			user.groups.add(Group.objects.get(name='norm_users'))
			user.save()
			new_pass = hashlib.md5(user_pass).hexdigest()
			form_new_user = user_table(username=user_email,password=new_pass)
			form_new_user.save()
			print 'hakunamana 2'
			user_group = group_table.objects.get(permissions=1)
			new_user_obj = user_info(user=form_new_user,first_name=user_firstname,last_name=user_lastname,group=user_group)
			new_user_obj.save()
			return HttpResponseRedirect('../../admin/')
