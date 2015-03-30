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
from django.http import Http404
from models import *
from datetime import datetime
import json
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

@csrf_exempt
def fill_form(request,**kwargs):
	if request.method == 'GET':
		form_hash_id = kwargs.get('form_hash')
		print form_hash_id
		f_obj = form_object_table.objects.filter(form_url = form_hash_id)
		print f_obj
		if len(f_obj) is 0 :
			raise Http404('Form Not Found.')
		if f_obj[0].flag is False:
			raise Http404('Form not active.')
		else:
			f_obj = f_obj[0]
			print f_obj.form_id
			print f_obj.form_title
			f_elements = elements_table.objects.filter(form_object = f_obj).order_by('priority')
			f_title = f_obj.form_title
			f_desc = f_obj.form_description
			render_list = list()
			for ele in f_elements:
				ndict = dict()
				ndict['title'] = ele.title
				ndict['description'] = ele.description
				ndict['required'] = ele.required
				ndict['input_type'] = ele.Input.input_type 
				ndict['id']= ele.elements_id
				render_list.append(ndict)
			print render_list
			return render_to_response('display.html',{'title':f_title,'description':f_desc,'elements':render_list})

	if request.method == 'POST':
		form_hash_id = kwargs.get('form_hash')
		print form_hash_id
		f_obj = form_object_table.objects.filter(form_url = form_hash_id)
		print f_obj
		if len(f_obj) is 0:
			raise Http404('Some Error Occured!!')
		else:
			f_obj = f_obj[0]
			user_ = None
			if not request.user.is_authenticated():
				user_ = user_table.objects.get(username='anonymous@anon.com')
			else:
				user_ = user_table.objects.get(username = request.user.email)
			elements_list = elements_table.objects.filter(form_object = f_obj)
			for elements in elements_list:
				ele_string = request.POST.get(str(elements.elements_id))	
				response = response_object_table(user=user_,form=f_obj.form,elements = elements,response_string = ele_string,response_time=datetime.now())
				response.save()
			return render_to_response('thanks.html',{'form_resubmit':request.get_full_path()})

@csrf_exempt
def view_form(request, **kwargs):
	if not request.user.is_authenticated():
		raise Http404('Please Log in to view this form')
	else:
		
		form_hash_id = kwargs.get('form_hash')
		f_obj = form_object_table.objects.filter(response_url = form_hash_id)
		if len(f_obj) is 0:
			raise Http404('Form not found')
		else:
			f_obj = f_obj[0]
			response_list = response_object_table.objects.filter(form=f_obj.form)
			render_list = list()
			element_list = list()
			for response in response_list:
				if not response.elements.title in element_list:
					element_list.append(response.elements.title)
			ndict = dict()
			for element_title in element_list:
				ndict[element_title] = ' '
			for response in response_list:
				ndict['username'] = response.user.username
				ndict[response.elements.title] = response.response_string
				ndict['Submission Time'] = str(response.response_time)
				print json.dumps(ndict)
				ndict['username'] = ''
				ndict['Submission Time'] = ''
			return render_to_response('spreadsheet.html',{'form_title':f_obj.form_title, 'response':json.dumps(ndict)})
