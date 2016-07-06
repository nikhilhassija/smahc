from django.contrib import admin
from .models import Medicine, Log, Glog

# Register your models here.

admin.site.register(Medicine)
admin.site.register(Log)
admin.site.register(GLog)