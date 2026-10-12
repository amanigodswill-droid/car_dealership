from django.contrib.auth.models import User
from django.db import models


class Car(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cars')
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.TextField()
    image = models.ImageField(upload_to='cars/', blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.brand} {self.model}"

class SellerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True)
    location = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.user.username

class CustomerReview(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='customer_reviews')
    seller = models.ForeignKey(User,on_delete=models.CASCADE, related_name='seller_reviews')
    rating = models.PositiveSmallIntegerField(
        choices=[
            (1, '1 Star'),
            (2, '2 Stars'),
            (3, '3 Stars'),
            (4, '4 Stars'),
            (5, '5 Stars'),
        ]
    )
    comment = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('customer', 'seller')
        ordering = ['-date_added']

    def __str__(self):
        return f"Review by {self.customer.username} for {self.seller.username}"

class CarSale(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    car = models.ForeignKey(Car, on_delete=models.PROTECT, related_name='sales')
    buyer = models.ForeignKey(User, on_delete=models.PROTECT, related_name='car_purchases')
    seller = models.ForeignKey(User, on_delete=models.PROTECT, related_name='car_sales')  
    agreed_price = models.DecimalField(max_digits=12,decimal_places=2)
    status = models.CharField(max_length=10,choices=STATUS_CHOICES,default='pending')
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.car} - {self.buyer.username} - {self.status}"