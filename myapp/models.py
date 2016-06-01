from django.db import models

# Create your models here.
class Medicine(models.Model):
	name = models.CharField(max_length=200)
	quantity = models.IntegerField(default=0)

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