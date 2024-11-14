from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from collection.models import Product
from profiles.models import UserProfile

class ProductReview(models.Model):
    class Meta:
        verbose_name_plural = 'Product Reviews'

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user_profile = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name='reviews'
    )
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Rate between 1 to 5"
    )
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(default=timezone.now, editable=False)

    def __str__(self):
        return f"{self.user_profile.user.username}'s review for {self.product.name}"
