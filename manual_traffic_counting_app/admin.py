from django.contrib import admin
from django.http import HttpResponse
from django.db.models import Count
import csv
from .models import CarType, CountingSession, CarCount

@admin.register(CarType)
class CarTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'image_tag')  

    def image_tag(self, obj):
        from django.utils.html import format_html
        if obj.image:
            return format_html('<img src="{}" width="80" height="50" />'.format(obj.image.url))
        return "No Image"
    image_tag.short_description = 'Image Preview'


@admin.register(CountingSession)
class CountingSessionAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_time', 'end_time', 'direction', 'streams', 'display_car_counts','display_car_types')
    readonly_fields = ('start_time', 'end_time', 'display_car_counts', 'streams')
    actions = ['export_to_csv']
    
    def display_car_types(self, obj):
        return ", ".join([car_type.name for car_type in obj.car_types.all()])
    display_car_types.short_description = "Car Types"

    def display_car_counts(self, obj):
        car_counts = CarCount.objects.filter(session=obj).values('car_type__name').annotate(total=Count('car_type'))
        count_strings = [f"{car_count['car_type__name']}: {car_count['total']}" for car_count in car_counts]
        return ", ".join(count_strings)
    display_car_counts.short_description = "Car Counts"

    def export_to_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="counting_sessions.csv"'
        writer = csv.writer(response)

        writer.writerow(['Session Name', 'Start Time', 'End Time', 'Direction','Streams','Selected Car Types', 'Car Type Counts'])
        for session in queryset:
            car_counts = CarCount.objects.filter(session=session).values('car_type__name').annotate(total=Count('car_type'))
            count_strings = [f"{count['car_type__name']}: {count['total']}" for count in car_counts]
            writer.writerow([session.name, session.start_time, session.end_time, session.direction, session.streams, [car_type.name for car_type in session.car_types.all()],"; ".join(count_strings)])

        return response

    export_to_csv.short_description = "Export Selected Sessions to CSV"

    # Specify which fields to display in the detail view
    fields = ('name', 'direction', 'start_time', 'end_time', 'display_car_counts','streams')

@admin.register(CarCount)
class CarCountAdmin(admin.ModelAdmin):
    list_display = ('car_type', 'session', 'timestamp', 'stream_number')
    actions = ['export_car_counts_to_csv']  # Add the custom action

    def export_car_counts_to_csv(self, request, queryset):
        """
        This method exports selected CarCount objects to a CSV file.
        """
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="car_counts.csv"'
        writer = csv.writer(response)

        # Write the headers to the CSV file
        writer.writerow(['Car Type', 'Session Name', 'Timestamp', 'Stream Number'])

        # Write data rows for each selected CarCount object
        for car_count in queryset:
            writer.writerow([
                car_count.car_type.name,
                car_count.session.name,
                car_count.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                car_count.stream_number
            ])

        return response

    export_car_counts_to_csv.short_description = "Export selected car counts to CSV"
