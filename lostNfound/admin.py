from django.contrib import admin

# Register your models here.

from .models import Item,Claim,Person,Report

admin.site.register(Item)
admin.site.register(Claim)
admin.site.register(Person)
admin.site.register(Report)