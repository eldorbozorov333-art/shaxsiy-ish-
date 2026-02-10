from django.db import models
from django.db.models import Sum


class Product(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    image = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name


class Income(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="incomes")
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=12, decimal_places=2, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Kirim"
        verbose_name_plural = "Kirimlar"

    def save(self, *args, **kwargs):
        if not self.pk:  # faqat YANGI kirim bo‘lsa
            self.total_price = self.quantity * self.product.price
            self.product.quantity += self.quantity
            self.product.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Kirim: {self.product.name}"


class Outcome(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="outcomes")
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=12, decimal_places=2, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Chiqim"
        verbose_name_plural = "Chiqimlar"

    def save(self, *args, **kwargs):
        if not self.pk:  # faqat YANGI chiqim bo‘lsa
            self.total_price = self.quantity * self.product.price
            if self.product.quantity >= self.quantity:
                self.product.quantity -= self.quantity
            else:
                self.product.quantity = 0
            self.product.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Chiqim: {self.product.name}"


# === HISOBOT FUNKSIYALARI ===

def total_income_sum():
    return Income.objects.aggregate(total=Sum('total_price'))['total'] or 0


def total_outcome_sum():
    return Outcome.objects.aggregate(total=Sum('total_price'))['total'] or 0


def finished_products():
    return Product.objects.filter(quantity=0)
