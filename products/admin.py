from django.contrib import admin
from django.utils.html import format_html
from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # Columns visible in admin product list
    list_display = ('id', 'name', 'category', 'price', 'stock', 'is_deleted', 'preview_image', 'created_at')
    list_filter = ('category', 'is_deleted')
    search_fields = ('name', 'category', 'description')
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ('created_at', 'updated_at')

    # Custom field to preview product image in admin list view
    def preview_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" style="border-radius:5px; object-fit:cover;" />', obj.images.url)
        return "-"
    preview_image.short_description = "Image"

    # Optional: hide soft-deleted products for non-superusers
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            qs = qs.filter(is_deleted=False)
        return qs

    # Optional: default ordering (newest first)
    ordering = ('-created_at',)
