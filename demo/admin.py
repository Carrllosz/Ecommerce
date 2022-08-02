from django.contrib import admin
from .models import *

'''
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'image', 'description')
admin.site.register(Product)
'''
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(Favourite)

