from django.db import models
from django.db.models import Avg


class Category(models.Model):

    class Meta:
        verbose_name_plural = 'Categories'

    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)
    header = models.CharField(max_length=254, default="")
    description = models.TextField(null=True, blank=True)
    image = models.CharField(max_length=254, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name


class ShopByOption(models.Model):

    class Meta:
        verbose_name_plural = 'Shop By Options'

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='shop_by_options'
    )
    name = models.CharField(max_length=254)
    friendly_name = models.CharField(
        max_length=254,
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.category.name} - {self.name}"

    def get_friendly_name(self):
        return self.friendly_name


class ProductType(models.Model):
    class Meta:
        verbose_name_plural = 'Product Types'

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='product_types'
    )
    name = models.CharField(max_length=254)
    friendly_name = models.CharField(
        max_length=254,
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.category.name} - {self.name}"

    def get_friendly_name(self):
        return self.friendly_name


class Product(models.Model):
    category = models.ForeignKey(
        'Category',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    shop_by = models.ForeignKey(
        'ShopByOption',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    product_type = models.ForeignKey(
        'ProductType',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    name = models.CharField(max_length=254)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    rating = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        null=True,
        blank=True
    )
    has_sizes = models.BooleanField(default=False)
    sizes = models.JSONField(null=True, blank=True, default=list)
    stock = models.IntegerField(default=0)
    sku = models.CharField(max_length=50, unique=True)
    image = models.ImageField(null=True, blank=True)
    is_featured = models.BooleanField(default=False)
    is_special_offer = models.BooleanField(default=False)
    discount_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.name

    def update_average_rating(self):
        average_rating = self.reviews.aggregate(Avg('rating'))['rating__avg'] or 0  # noqa
        self.rating = round(average_rating, 1)
        self.save()
