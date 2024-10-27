from django.contrib import admin
from .models import Product, Category, ShopByOption, ProductType


# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'sku',
        'name',
        'get_categories',
        'shop_by', 
        'product_type',
        'price',
        'rating',
        'stock',
        'is_featured',
        'is_special_offer',
        'image',
    )
    
    ordering = ('sku',)
    
    def get_categories(self, obj):
        return ", ".join([category.friendly_name for category in obj.category.all()])
    get_categories.short_description = 'Categories'


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'friendly_name',
        'name',
    )


class ShopByOptionAdmin(admin.ModelAdmin):
    list_display = (
        'category',
        'friendly_name',
        'name',
    )


class ProductTypeAdmin(admin.ModelAdmin):
    list_display = (
        'category',
        'friendly_name',
        'name',
    )


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(ShopByOption, ShopByOptionAdmin)
admin.site.register(ProductType, ProductTypeAdmin)