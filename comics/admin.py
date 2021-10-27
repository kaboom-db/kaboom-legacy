from django.contrib import admin
from .models import Series, Issue, Publisher, Character, Staff

# Register your models here.
admin.site.register(Series)
admin.site.register(Issue)
admin.site.register(Publisher)
admin.site.register(Character)
admin.site.register(Staff)