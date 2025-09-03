from django.contrib import admin
from .models import Products


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'quantity')
    search_fields = ('name',)
    list_filter = ('price', 'quantity')
    ordering = ('name',)
    fields = ('name', 'photo', 'price', 'description', 'quantity')
    readonly_fields = ('photo',)

admin.site.register(Products, ProductAdmin)