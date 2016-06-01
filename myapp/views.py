from django.shortcuts import render
from django.http import HttpResponse

from .models import Medicine, Log
# Create your views here.

def index(request):
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

def login(request):
	return HttpResponse("Login here")

def add(request):
	return HttpResponse("Add medicines to stock")

def issue(request):
	return HttpResponse("Issue medicines from stock")

def inventory(request):
	m = sorted(Medicine.objects.all(), key=lambda x: x.name)
	context = {'medicines':m}
	return render(request,'inventory.html',context)

def new_medicine(request):
	return HttpResponse("Add new med to system")

def change_critical_quantity(request,medicine_id):
	return HttpResponse("Add new med to system")

def view_medicine(request,medicine_id):
	m = Medicine.objects.get(pk=medicine_id)
	l = sorted(m.log_set.all(), key=lambda x: x.date, reverse=True)
	ldate = []
	ltype = []
	ldelt = []

	for i in l:
		if i.quantity_change != 0:
			ldate.append(i.date.date())
			if(i.quantity_change < 0):
				ltype.append("Issued")
				ldelt.append(-i.quantity_change)
			else:
				ltype.append("Added")
				ldelt.append(i.quantity_change)

	l = list(zip(ldate,ltype,ldelt))
	context = {'medicine':m, 'logs':l}
	return render(request,'medicine.html',context)