from django.contrib import admin
from .models import Products
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'quantity')
    search_fields = ('name',)
    list_filter = ('price', 'quantity')
    ordering = ('name',)
    fields = ('name', 'photo', 'price', 'description', 'quantity')
    readonly_fields = ('photo',)

admin.site.register(Products, ProductAdmin)