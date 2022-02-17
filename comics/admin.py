from django.contrib import admin
from .models import Comic, Format, Issue, Publisher, Character, Staff, StaffPositions

# Register your models here.
admin.site.register(StaffPositions)
admin.site.register(Format)

@admin.register(Comic)
class ComicAdmin(admin.ModelAdmin):
    list_display = ("series_name", "publisher", "year_started", "status", "rating")
    
    def get_readonly_fields(self, request, obj=None):
        if obj:
            if not request.user.is_superuser:
                return self.readonly_fields + ('cover_image', 'background_image', 'rating', 'date_created')
        return self.readonly_fields + ('rating', 'date_created')

@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    list_display = ("issue_number", "issue_number_absolute", "series", "format", "release_date", "date_created")

    def get_readonly_fields(self, request, obj=None):
        if obj:
            if not request.user.is_superuser:
                return self.readonly_fields + ('cover_image', 'date_created')
        return self.readonly_fields + ('date_created',)

@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    list_display = ("name", "website", "date_created")

    def get_readonly_fields(self, request, obj=None):
        if obj:
            if not request.user.is_superuser:
                return self.readonly_fields + ('logo', 'date_created')
        return self.readonly_fields + ('date_created',)

@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ("name", "position", "date_of_birth", "date_of_death", "date_created")

    def get_readonly_fields(self, request, obj=None):
        if obj:
            if not request.user.is_superuser:
                return self.readonly_fields + ('image', 'date_created')
        return self.readonly_fields + ('date_created',)