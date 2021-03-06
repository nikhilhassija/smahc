from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Medicine(models.Model):
	name = models.CharField(max_length=200)
	quantity = models.IntegerField(default=0)
	critical_quantity = models.IntegerField(default=10)
	monthly_usage = models.IntegerField(default=1000)

	def __str__(self):
		return self.name

class Log(models.Model):
	medicine = models.ForeignKey(Medicine,on_delete=models.CASCADE)
	date = models.DateTimeField('date:')
	quantity_change = models.IntegerField()

	def __str__(self):
		if(self.quantity_change < 0):
			return "Issued {} {} on {}".format(-self.quantity_change,self.medicine.name,self.date)
		else:
			return "Added {} {} on {}".format(self.quantity_change,self.medicine.name,self.date)

class GLog(models.Model):
	user = models.ForeignKey(User)
	date = models.DateTimeField()
	actn = models.CharField(max_length=1000)

	def __str__(self):
		return "{} | {} | {}".format(self.date,self.user,self.actn)