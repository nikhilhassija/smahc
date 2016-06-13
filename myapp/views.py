from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Medicine, Log
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout

# Create your views here.

message = []
err_mes = []

def index(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect("login")
	m = sorted(Medicine.objects.all(), key=lambda x: x.name)
	mname = []
	mqty  = []
	for i in m:
		if i.quantity <= i.critical_quantity:
			mname.append(i.name)
			mqty.append(i.quantity)
	mzip = list(zip(mname,mqty))
	context = {'medicines':mzip}
	return render(request,'index.html',context)

def login_view(request):
	if request.user.is_authenticated():
		return HttpResponseRedirect("/")		
	
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username,password=password)
		if user is not None:
			login(request,user)
			return HttpResponseRedirect("/")		
		
	return render(request,'login.html')

def logout_view(request):
	logout(request)
	return HttpResponseRedirect("login")

def add(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect("login")
	if request.method == 'POST':
		global message
		message = []
		s = request.POST['str']
		s = s.split('|')
		s = s[:-1]
		s.append("{},{}".format(request.POST['quantity1'],request.POST['medicine1']))
		for i in s:
			i = i.split(',')
			i[0] = int(i[0])
			m = Medicine.objects.get(name=i[1])
			m.quantity += i[0]
			m.log_set.create(date=timezone.now(),quantity_change=i[0])
			m.save()
			message.append("Added {} {}.".format(i[0],m.name))
		return HttpResponseRedirect('success')
	
	m = sorted(Medicine.objects.all(), key=lambda x: x.name)
	context = {'medicines':m, 'range':[0]*1000}
	return render(request,'add.html',context)

def success(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect("login")
	global message
	context = {'message':message}
	message = []
	return render(request,'success.html',context)

def error(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect("login")
	global err_mes
	context = {'message':err_mes}
	err_mes = []
	return render(request,'error.html',context)

def issue(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect("login")
	if request.method == 'POST':
		global message
		global err_mes
		message = []
		err_mes = []
		s = request.POST['str']
		s = s.split('|')
		s = s[:-1]
		s.append("{},{}".format(request.POST['quantity1'],request.POST['medicine1']))
		for i in s:
			i = i.split(',')
			i[0] = int(i[0])
			m = Medicine.objects.get(name=i[1])
			if i[0] > m.quantity:
				err_mes.append("Not enough stock of {} available. Current Quantity: {}".format(m.name,m.quantity))
		if err_mes:
			return HttpResponseRedirect('error') 
		for i in s:
			i = i.split(',')
			i[0] = int(i[0])
			m = Medicine.objects.get(name=i[1])
			m.quantity -= i[0]
			m.log_set.create(date=timezone.now(),quantity_change=-i[0])
			m.save()
			message.append("Issued {} {}.".format(i[0],m.name))
		return HttpResponseRedirect('success')
	
	m = sorted(Medicine.objects.all(), key=lambda x: x.name)
	context = {'medicines':m, 'range':[0]*1000}
	return render(request,'issue.html',context)

def inventory(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect("login")
	m = sorted(Medicine.objects.all(), key=lambda x: x.name)
	context = {'medicines':m}
	return render(request,'inventory.html',context)

def new_medicine(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect("login")
	if request.method == 'POST':
		mname = request.POST['medicine_name']
		mcrit = int(request.POST['medicine_critical_quantity'])
		minit = int(request.POST['medicine_initial_quantity'])
		m = Medicine.objects.all()
		for i in m:
			if i.name == mname:
				global err_mes
				err_mes = []
				err_mes.append("{} already exists!".format(mname))
				return HttpResponseRedirect("error")
		m = Medicine(name=mname,critical_quantity=mcrit,quantity=minit)
		m.save()
		global message
		message = []
		message.append("Added {} to inventory".format(mname))
		return HttpResponseRedirect("success") 
	return render(request,'new_medicine.html')

def change_critical_quantity(request,medicine_id):
	if not request.user.is_authenticated():
		return HttpResponseRedirect("login")
	if request.method == 'POST':
		m = Medicine.objects.get(pk=medicine_id)
		m.critical_quantity = request.POST['new_critical_quantity']
		m.save()
		return HttpResponseRedirect('view_medicine/{}'.format(medicine_id))
	m = Medicine.objects.get(pk=medicine_id)
	context = {'medicine':m}
	return render(request,'change.html',context)

def view_medicine(request,medicine_id):
	if not request.user.is_authenticated():
		return HttpResponseRedirect("login")
	m = Medicine.objects.get(pk=medicine_id)
	l = sorted(m.log_set.all(), key=lambda x: x.date, reverse=True)
	ldate = []
	l_add = []
	l_sub = []
	l_qnt = []
	q = m.quantity
	for i in l:
		if i.quantity_change != 0:
			ldate.append(i.date.date())
			l_add.append(max(0,i.quantity_change))
			l_sub.append(-min(0,i.quantity_change))
			l_qnt.append(q)
			q -= i.quantity_change

	l = list(zip(ldate,l_add,l_sub,l_qnt))
	context = {'medicine':m, 'logs':l}
	return render(request,'medicine.html',context)