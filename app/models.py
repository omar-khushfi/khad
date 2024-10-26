from django.db import models

# Create your models here.
class Product(models.Model):
    title=models.CharField(max_length=50)
    price=models.DecimalField(max_digits=5,decimal_places=2)
    simple_discription=models.CharField(max_length=200)
    discription=models.CharField(max_length=4000)
    image=models.ImageField(upload_to='photo')
    def __str__(self):
       return self.title

class Order(models.Model):
	name=models.CharField(max_length=40)
	total=models.DecimalField(max_digits=6,decimal_places=2)
	email=models.EmailField()
	phone_number=models.IntegerField()
	date=models.DateTimeField(auto_now=True)
	
	def __str__(self):
		return self.name+"___"+str(self.date)
	
 

    
class product_in_order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def subtotal(self):
        return self.product.price * self.quantity if self.product.price and self.quantity else 0

    def __str__(self):
        return f"{self.order.name}___{self.product.title}"