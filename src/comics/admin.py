from django.contrib import admin
from .models import Comic, Issue, Publisher, Character, Staff, StaffPositions

# Register your models here.
admin.site.register(Comic)
admin.site.register(Issue)
admin.site.register(Publisher)
admin.site.register(Character)
admin.site.register(Staff)
admin.site.register(StaffPositions)