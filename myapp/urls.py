from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'add',views.add,name='add'),
	url(r'^$', views.index, name='index'),
	url(r'issue',views.issue,name='issue'),
	url(r'error',views.error,name='error'),
	url(r'success',views.success,name='success'),
	url(r'login',views.login_view,name='login'),
	url(r'logout',views.logout_view,name='logout'),
	url(r'inventory',views.inventory,name='issue'),
	url(r'new_medicine',views.new_medicine,name='new_med'),
	url(r'medicine/(?P<medicine_id>[0-9]+)',views.view_medicine,name='view_medicine'),	
	url(r'change_critical_quantity/(?P<medicine_id>[0-9]+)',views.change_critical_quantity,name='change_critical_quantity'),	
]