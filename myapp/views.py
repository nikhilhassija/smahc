from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Medicine, Log
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

import csv

# Create your views here.

message = []
err_mes = []

@login_required(login_url="/login/")
def index(request):
	m = sorted(Medicine.objects.all(), key=lambda x: x.name)
	mid  = []
	mqty  = []
	mname = []
	for i in m:
		if i.quantity <= i.critical_quantity:
			mid.append(i.id)
			mname.append(i.name)
			mqty.append(i.quantity)
	
	mzip = zip(mid,mname,mqty)
	context = {'medicines':mzip, 'date':timezone.now().date()}
	return render(request,'index.html',context)

def login_view(request):
	
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username,password=password)
		if user is not None:
			login(request,user)
			return HttpResponseRedirect("/")		
		
	return render(request,'login.html')

@login_required(login_url="/login/")
def logout_view(request):
	logout(request)
	return HttpResponseRedirect("login")

@login_required(login_url="/login/")
def add(request):
	if request.method == 'POST':
		global message
		message = []
		s = request.POST['str']
		s = s.split('|')
		s = s[:-1]
		# s.append("{},{}".format(request.POST['quantity1'],request.POST['medicine1']))
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

@login_required(login_url="/login/")
def success(request):
	global message
	context = {'message':message}
	message = []
	return render(request,'success.html',context)

@login_required(login_url="/login/")
def error(request):
	global err_mes
	context = {'message':err_mes}
	err_mes = []
	return render(request,'error.html',context)

@login_required(login_url="/login/")
def issue(request):
	if request.method == 'POST':
		global message
		global err_mes
		message = []
		err_mes = []
		s = request.POST['str']
		s = s.split('|')
		s = s[:-1]
		# s.append("{},{}".format(request.POST['quantity1'],request.POST['medicine1']))
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

@login_required(login_url="/login/")
def inventory(request):
	m = sorted(Medicine.objects.all(), key=lambda x: x.name)
	context = {'medicines':m}
	return render(request,'inventory.html',context)

@login_required(login_url="/login/")
def new_medicine(request):
	if request.method == 'POST':
		mname = request.POST['medicine_name']
		mous = int(request.POST['medicine_monthly_usage'])
		mcrit = int(request.POST['medicine_critical_quantity'])
		minit = int(request.POST['medicine_initial_quantity'])
		m = Medicine.objects.all()
		for i in m:
			if i.name == mname:
				global err_mes
				err_mes = []
				err_mes.append("{} already exists!".format(mname))
				return HttpResponseRedirect("error")
		m = Medicine(name=mname,monthly_usage=mous,critical_quantity=mcrit,quantity=minit)
		m.save()
		global message
		message = []
		message.append("Added {} to inventory".format(mname))
		return HttpResponseRedirect("success") 
	return render(request,'new_medicine.html')

@login_required(login_url="/login/")
def edit_medicine(request,medicine_id):
	if request.method == 'POST':
		m = Medicine.objects.get(pk=medicine_id)
		m.name = request.POST['new_name']
		m.critical_quantity = request.POST['new_critical_quantity']
		m.monthly_usage = request.POST['new_monthly_usage']
		m.save()
		return HttpResponseRedirect('/medicine/{}'.format(medicine_id))
	m = Medicine.objects.get(pk=medicine_id)
	context = {'medicine':m}
	return render(request,'change.html',context)

@login_required(login_url="/login/")
def view_medicine(request,medicine_id):
	m = Medicine.objects.get(pk=medicine_id)
	l = sorted(m.log_set.all(), key=lambda x: x.date, reverse=True)
	ldate = []
	l_add = []
	l_sub = []
	l_qnt = []
	l_tag = []
	q = m.quantity
	for i in l:
		if i.quantity_change != 0:
			ldate.append(i.date.date())
			l_add.append(max(0,i.quantity_change))
			l_sub.append(-min(0,i.quantity_change))
			l_qnt.append(q)
			if i.quantity_change < 0:
				l_tag.append("danger")
			else:
				l_tag.append("success")
			q -= i.quantity_change

	l = zip(l_tag,ldate,l_add,l_sub,l_qnt)
	context = {'medicine':m, 'logs':l}
	return render(request,'medicine.html',context)


@login_required(login_url="/login/")
def restock(request):
	m = sorted(Medicine.objects.all(), key=lambda x:x.name)
	n = 0

	ma = []
	na = []

	mb = []

	for i in m:
		if i.quantity < i.monthly_usage:
			ma.append(i)
			na.append(i.monthly_usage - i.quantity)
			n += 1
		else:
			mb.append(i)

	ma = zip(ma,na)

	context = {'ma':ma, 'mb':mb, 'num':n}

	return render(request,'restock.html',context)

	
@login_required(login_url="/login/")
def report(request,daterange=None,format=None):
	if request.method == 'POST':
		d = request.POST['startdate'] + request.POST['enddate'] 
		d = d.replace("-","")

		f = int(request.POST['csv'])

		if f:
			f = "csv"
		else:
			f = ""	
		if(len(d) == 16):
			return HttpResponseRedirect("report/{}/{}".format(d,f))

	if daterange and len(daterange) == 16:
		sdate = str(daterange)[:8]
		fsdate = "{}/{}/{}".format(sdate[-2:],sdate[-4:-2],sdate[:4])

		edate = str(daterange)[8:]
		fedate = "{}/{}/{}".format(edate[-2:],edate[-4:-2],edate[:4])

		s_int = int(sdate)
		e_int = int(edate)

		if e_int < s_int:
			return HttpResponseRedirect("report")

		mset = sorted(Medicine.objects.all(), key=lambda x:x.name)
		uset = []

		for m in mset:
			lset = m.log_set.all()
			u = 0
			for l in lset:
				d = int(l.date.date().strftime("%Y%m%d"))
				if s_int <= d and d <= e_int:
					u += (-min(0,l.quantity_change))
			uset.append(u)

		mset = zip(mset,uset)

		if format == "csv":
			response = HttpResponse(content_type='text/csv')
			response['Content-Disposition'] = 'attachment; filename="report{}.csv"'.format(daterange)

			writer = csv.writer(response)
			
			writer.writerow(["Medicine","Usage"])
			for m,u in mset:
				writer.writerow([m.name,u])

			return response
		else:
			context = {'view':True, 'start':fsdate,'end':fedate,'medicines':mset,'f':format}
			return render(request,'report.html',context)

	return render(request,'report.html')