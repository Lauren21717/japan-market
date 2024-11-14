from django.contrib import admin
from .models import ProductReview


class ProductReviewAdmin(admin.ModelAdmin):
    readonly_fields = (
        'product',
        'user_profile',
        'rating',
        'comment',
        'created_at',
    )


admin.site.register(ProductReview, ProductReviewAdmin)