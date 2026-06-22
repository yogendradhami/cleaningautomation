from django.contrib import admin
from .models import Enquiry


@admin.register(Enquiry)
class EnquiryAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'email', 'message')
    actions = ['export_as_csv']

    def export_as_csv(self, request, queryset):
        import csv
        from django.http import HttpResponse

        meta = self.model._meta
        field_names = ['name', 'email', 'message', 'created_at']

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=enquiries.csv'

        writer = csv.writer(response)
        writer.writerow(field_names)
        for obj in queryset:
            writer.writerow([getattr(obj, f) for f in field_names])
        return response
    export_as_csv.short_description = "Export selected enquiries as CSV"
    

from .models import EnquiryImage


class EnquiryImageInline(admin.TabularInline):
    model = EnquiryImage
    extra = 0


EnquiryAdmin.inlines = [EnquiryImageInline]
