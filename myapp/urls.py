from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
	url(r'add',views.add,name='add'),
	url(r'^$', views.index, name='index'),
	url(r'issue',views.issue,name='issue'),
	url(r'error',views.error,name='error'),
	url(r'report$',views.report,name='report'),
	url(r'login',views.login_view,name='login'),
	url(r'restock',views.restock,name='restock'),
	url(r'success',views.success,name='success'),
	url(r'logout',views.logout_view,name='logout'),
	url(r'inventory',views.inventory,name='issue'),
	url(r'new_medicine',views.new_medicine,name='new_med'),
	url(r'report/(?P<daterange>[0-9]+)/(?P<format>[a-z]*)',views.report,name='report'),
	url(r'^medicine/(?P<medicine_id>[0-9]+)',views.view_medicine,name='view_medicine'),	
	url(r'edit_medicine/(?P<medicine_id>[0-9]+)',views.edit_medicine,name='edit_medicine'),	
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)