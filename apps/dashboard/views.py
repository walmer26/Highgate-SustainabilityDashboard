from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.shortcuts import render
from django.db.models import Sum, Max
from .models import Service
import io
import base64
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


@login_required
def dashboard_view(request):
    # Define cache keys
    all_locations_cache_key = 'all_locations'
    all_service_types_cache_key = 'all_service_types'

    # Fetch all unique locations and service types from cache or database
    all_locations = cache.get_or_set(
        all_locations_cache_key,
        lambda: list(Service.objects.values_list('location__name', flat=True).distinct()),
        60 * 15
    )

    all_service_types = cache.get_or_set(
        all_service_types_cache_key,
        lambda: list(Service.objects.values_list('service_type', 'uom').distinct()),
        60 * 15
    )

    latest_year = Service.objects.aggregate(Max('year'))['year__max']

    # Fetch all services for the latest year in a single query
    services = Service.objects \
                .select_related('location', 'vendor', 'account', 'meter', 'rate_schedule') \
                .filter(year=latest_year) \
                .values('location__name', 'month', 'service_type', 'uom') \
                .annotate(total_usage=Sum('usage')) \
                .order_by('location__name', 'month', 'service_type')

    # Prepare data structures for plots and summary tables
    data = {location: {service_type: 0 for service_type, _ in all_service_types} for location in all_locations}
    location_data = {}
    service_types_set = set()

    for entry in services:
        location_name = entry['location__name']
        month = entry['month']
        service_type = entry['service_type']
        uom = entry['uom']
        total_usage = float(entry['total_usage'])

        # Update data for plots
        data[location_name][service_type] += total_usage

        # Update data for summary tables
        if location_name not in location_data:
            location_data[location_name] = {}
        if month not in location_data[location_name]:
            location_data[location_name][month] = {}
        location_data[location_name][month][service_type] = total_usage
        service_types_set.add(service_type)

    # Convert the set of service types to a sorted list
    service_types = sorted(service_types_set)

    # Create plots
    plots = []
    for service_type, uom in all_service_types:
        # Get the top 25 locations by total usage for each service type
        filtered_data = {loc: usage for loc, usage in data.items() if usage[service_type] > 0}
        top_locations = sorted(filtered_data.keys(), key=lambda x: filtered_data[x][service_type], reverse=True)[:25]

        if not top_locations:
            continue

        # Create a horizontal bar plot for each service type
        fig, ax = plt.subplots(figsize=(20, 12))
        bar_height = 0.35  # Adjusted bar height
        index = range(len(top_locations))

        usage_values = [filtered_data[loc][service_type] for loc in top_locations]
        ax.barh(index, usage_values, bar_height, label=service_type)

        ax.set_ylabel('Locations', fontsize=16)
        ax.set_xlabel(f'Total Usage ({uom})', fontsize=16)
        ax.set_title(f'Service Type: {service_type} Usage Summary for Top 25 Properties ({uom})', fontsize=16)
        ax.set_yticks(index)
        ax.set_yticklabels(top_locations, fontsize=16)
        ax.legend()

        # Adjust x-axis limits and add gridlines
        max_usage = max(usage_values) if usage_values else 0
        ax.set_xlim(0, max_usage * 1.1)  # Set x-axis limits with a 10% margin
        ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x:,.0f}'))  # Format x-axis values
        ax.grid(True, which='both', linestyle='--', linewidth=0.5)

        plt.tight_layout()

        # Save the plot to a BytesIO object
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        plt.close(fig)
        buffer.seek(0)
        image_png = buffer.getvalue()
        buffer.close()

        # Encode the image to base64
        image_base64 = base64.b64encode(image_png).decode('utf-8')
        plots.append((service_type, image_base64, uom))

    context = {
        'year': latest_year,
        'plots': plots,
        'location_data': location_data,
        'service_types': service_types,
    }

    # Render the plots and the summary tables in the template
    return render(request, 'dashboard/dashboard.html', context)
