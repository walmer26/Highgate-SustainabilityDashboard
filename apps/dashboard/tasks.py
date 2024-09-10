from background_task import background
from django.core.cache import cache
from apps.dashboard.models import Location, Vendor, Account, RateSchedule, Service
from utils.data_parsers.use_cost_csv_parser import parse_csv
from datetime import datetime
from decimal import Decimal

@background(schedule=0)  # This schedules the task to run immediately
def populate_data(file_path):
    data = parse_csv(file_path)

    # Caching to avoid repeated queries
    locations_cache = {}
    vendors_cache = {}
    accounts_cache = {}
    rate_schedules_cache = {}
    services_to_create = []

    BATCH_SIZE = 1000
    record_count = 0
    cumulative_record_count = 0

    # Loop over each record in the parsed CSV data
    for record in data:
        # Handle Location creation or retrieval
        location_name = record['Location Name']
        if location_name not in locations_cache:
            location, created = Location.objects.get_or_create(
                name=location_name,
                defaults={
                    'location_number': record['Location #'],
                    'total_bldg_sqft': record['Total Bldg SqFt'],
                }
            )
            locations_cache[location_name] = location
        else:
            location = locations_cache[location_name]

        # Handle Vendor creation or retrieval
        vendor_name = record['Vendor Name']
        if vendor_name not in vendors_cache:
            vendor, created = Vendor.objects.get_or_create(name=vendor_name)
            vendor.locations.add(location)
            vendors_cache[vendor_name] = vendor
        else:
            vendor = vendors_cache[vendor_name]
            vendor.locations.add(location)

        # Handle Account creation or retrieval
        account_number = record['Account #']
        if account_number not in accounts_cache:
            account, created = Account.objects.get_or_create(
                account_number=account_number,
                defaults={
                    'supplier_only_account': record['Supplier Only Account'].lower() == 'true',
                    'audit_only': record['Audit Only'].lower() == 'yes',
                    'location': location
                }
            )
            accounts_cache[account_number] = account
        else:
            account = accounts_cache[account_number]

        # Handle RateSchedule creation or retrieval
        rate_schedule_value = record['Rate Schedule']
        if rate_schedule_value:
            if rate_schedule_value not in rate_schedules_cache:
                rate_schedule, created = RateSchedule.objects.get_or_create(
                    rate_schedule=rate_schedule_value
                )
                rate_schedule.locations.add(location)
                rate_schedules_cache[rate_schedule_value] = rate_schedule
            else:
                rate_schedule = rate_schedules_cache[rate_schedule_value]
                rate_schedule.locations.add(location)
        else:
            rate_schedule = None

        # Parse the date and create the Service record
        valid_date = datetime.strptime(str(record['Month']), '%m/%d/%Y').date()

        service = Service(
            location=location,
            vendor=vendor,
            account=account,
            rate_schedule=rate_schedule,
            month=valid_date.month,
            year=valid_date.year,
            service_days=int(record['Service Days']),
            cost=Decimal(record['Cost']),
            service_type=record['Service Type'],
            uom=record['UOM'],
            usage=Decimal(record['Usage']),
            kbtus=Decimal(record['KBTUs']),
            open_exceptions=record['Open Exceptions'].lower() == 'yes',
            bundle=record['Bundle'],
            entity=record['Entity']
        )
        service.hash = service.get_hash()

        # Check for duplicates using the hash
        if not Service.objects.filter(hash=service.hash).exists():
            services_to_create.append(service)
            record_count += 1
            cumulative_record_count += 1

            # Bulk create when batch size is reached
            if record_count >= BATCH_SIZE:
                Service.objects.bulk_create(services_to_create, ignore_conflicts=False)
                services_to_create = []
                record_count = 0

    # Insert any remaining services
    if services_to_create:
        Service.objects.bulk_create(services_to_create, ignore_conflicts=False)

    # Set a message in the cache to be picked up by the middleware
    if cumulative_record_count > 0:
        cache.set('task_completion_message', f"{cumulative_record_count} records populated successfully!", timeout=60*15)
    else:
        cache.set('task_completion_message', 'No records to populate!', timeout=60*15)
