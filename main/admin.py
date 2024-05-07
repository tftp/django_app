from django.contrib import admin

from main.models import Product, ProductType, Customer


# Register your models here.

@admin.register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    list_display = "pk", "name"
    list_display_links = "name",
    ordering = "pk",


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = "identity_number", "name", "product_type"
    list_display_links = "name",
    ordering = "identity_number",
    search_fields = "identity_number", "name"

    def get_queryset(self, request):
        return Product.objects.select_related("producttype")

    def product_type(self, obj: Product) -> str:
        return obj.producttype.name

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = "fio", "telephone", "house_auditory", "archived"
    list_display_links = "fio",
    ordering = "surname",
    search_fields = "fio",

