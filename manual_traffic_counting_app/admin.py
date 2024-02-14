from django.contrib import admin
from django.http import HttpResponse
from django.db.models import Count
from django.utils.html import format_html
import csv
from .models import CarType, CountingSession, CarCount

@admin.register(CarType)
class CarTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)

from django.utils.html import format_html

@admin.register(CountingSession)
class CountingSessionAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_time', 'end_time', 'direction', 'display_car_counts')
    readonly_fields = ('start_time', 'end_time', 'display_car_counts_detail',)
    actions = ['export_to_csv']

    def display_car_counts_detail(self, obj):
        car_counts = CarCount.objects.filter(session=obj).values('car_type__name').annotate(total=Count('car_type'))
        count_strings = [f"{car_count['car_type__name']}: {car_count['total']}" for car_count in car_counts]
        return ", ".join(count_strings)
    display_car_counts_detail.short_description = "Car Counts"

    def display_car_counts(self, obj):
        car_counts = CarCount.objects.filter(session=obj).values('car_type__name').annotate(total=Count('car_type'))
        count_strings = [f"{car_count['car_type__name']}: {car_count['total']}" for car_count in car_counts]
        return ", ".join(count_strings)
    display_car_counts.short_description = "Car Counts"

    def export_to_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="counting_sessions.csv"'
        writer = csv.writer(response)

        writer.writerow(['Session Name', 'Start Time', 'End Time', 'Direction', 'Car Type Counts'])
        for session in queryset:
            car_counts = CarCount.objects.filter(session=session).values('car_type__name').annotate(total=Count('car_type'))
            count_strings = [f"{count['car_type__name']}: {count['total']}" for count in car_counts]
            writer.writerow([session.name, session.start_time, session.end_time, session.direction, "; ".join(count_strings)])

        return response

    export_to_csv.short_description = "Export Selected Sessions to CSV"

    # Specify which fields to display in the detail view
    fields = ('name', 'direction', 'start_time', 'end_time', 'display_car_counts_detail',)

@admin.register(CarCount)
class CarCountAdmin(admin.ModelAdmin):
    list_display = ('car_type', 'session', 'timestamp')
    actions = ['export_car_counts_to_csv']  # Add the custom action

    def export_car_counts_to_csv(self, request, queryset):
        """
        This method exports selected CarCount objects to a CSV file.
        """
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="car_counts.csv"'
        writer = csv.writer(response)

        # Write the headers to the CSV file
        writer.writerow(['Car Type', 'Session Name', 'Timestamp'])

        # Write data rows for each selected CarCount object
        for car_count in queryset:
            writer.writerow([
                car_count.car_type.name,
                car_count.session.name,
                car_count.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            ])

        return response

    export_car_counts_to_csv.short_description = "Export selected car counts to CSV"
