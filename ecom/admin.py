from django.contrib import admin
from .models import Products, Payment
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

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'transcation_uuid', 'amount', 'quantity', 'status', 'created_at')
    search_fields = ('transcation_uuid', 'user__username', 'product__name')
    list_filter = ('status', 'created_at')
    ordering = ('-created_at',)
    fields = ('user', 'product', 'transcation_uuid', 'amount', 'quantity', 'status', 'created_at')
    readonly_fields = ('created_at',)

admin.site.register(Payment, PaymentAdmin)
