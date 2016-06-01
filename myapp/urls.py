from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'add',views.add,name='add'),
	url(r'issue',views.issue,name='issue'),
	url(r'inventory',views.inventory,name='issue'),
	url(r'new_medicine',views.new_medicine,name='new_med'),
	url(r'change_critical_quantity/(?P<medicine_id>[0-9]+)',views.change_critical_quantity,name='change_critical_quantity'),	
	url(r'medicine/(?P<medicine_id>[0-9]+)',views.view_medicine,name='view_medicine'),	
]