from django.contrib import admin
from store.models import Product, UserProductRelation


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass


@admin.register(UserProductRelation)
class UserProductRelationAdmin(admin.ModelAdmin):
    pass
