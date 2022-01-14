from django.contrib import admin
from .models import Comic, Format, Issue, Publisher, Character, Staff, StaffPositions

# Register your models here.
admin.site.register(StaffPositions)
admin.site.register(Format)

@admin.register(Comic)
class ComicAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        if obj:
            if not request.user.is_superuser:
                return self.readonly_fields + ('cover_image', 'background_image', 'rating')
        return self.readonly_fields + ('rating',)

@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        if obj:
            if not request.user.is_superuser:
                return self.readonly_fields + ('cover_image',)
        return self.readonly_fields

@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        if obj:
            if not request.user.is_superuser:
                return self.readonly_fields + ('logo',)
        return self.readonly_fields

@admin.register(Character)
class CharacterComicsAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        if obj:
            if not request.user.is_superuser:
                return self.readonly_fields + ('image',)
        return self.readonly_fields

@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        if obj:
            if not request.user.is_superuser:
                return self.readonly_fields + ('image',)
        return self.readonly_fields