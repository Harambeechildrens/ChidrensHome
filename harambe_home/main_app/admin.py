from django.contrib import admin
from .models import Child, Staff, Donor

# Register your models here.
admin.site.register(Child)
admin.site.register(Staff)
admin.site.register(Donor)
