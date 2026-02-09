from django.db import models

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=50)
    quantity = models.IntegerField()
    image = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name 
    

class Income(models.Model):   #kirim klasim 
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=12, decimal_places=2, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Kirim"
        verbose_name_plural = "Kirimlar"

    def save(self, *args, **kwargs):
        self.total_price = self.quantity * self.price
        self.product.quantity += self.quantity  #kirimlar qo'shilganda yangilaydi
        self.product.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Kirim: {self.product.name}"
    
class Outcome(models.Model): #chiqim klasi 
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=12, decimal_places=2, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Chiqim"
        verbose_name_plural = "Chiqimlar"

    def save(self, *args, **kwargs):
        self.total_price = self.quantity * self.price
        self.product.quantity -= self.quantity   # chiqimlar minus qilinadi
        if self.product.quantity < 0:
            self.product.quantity = 0  # 0 dan pastga tushmasligi kerak
        self.product.save()
        super().save(*args, **kwargs)
 
    def __str__(self):
        return f"Chiqim: {self.product.name}"


from django.db.models import Sum   # barcha kirim chiqimlarimni  hisoblash uchun 
def total_income_sum():
    return Income.objects.aggregate(total=Sum('total_price'))['total'] or 0
def total_outcome_sum():
    return Outcome.objects.aggregate(total=Sum('total_price'))['total'] or 0

def finished_products():  #mahsulot bor yuqligini bilib beradi
    return Product.objects.filter(quantity=0)

