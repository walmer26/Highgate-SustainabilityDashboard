from datetime import datetime
from csv_parser import process_folder
from decimal import Decimal


def parse_date(date_str):
    """Helper function to parse date strings into datetime objects."""
    return datetime.strptime(date_str, '%m/%d/%Y')


def accumulate_usage_per_unique_id_per_period(data):
    billing_data = {}

    for entry in data:
        unique_id = f"{entry['Location Name']}-{entry['Account #']}-{entry['Service Type']}"
        service_begin = parse_date(entry['Service Begin Date'])
        service_end = parse_date(entry['Service End Date'])
        usage = Decimal(entry['Usage'])

        # Initialize the dictionary for the unique_id if not already present
        if unique_id not in billing_data:
            billing_data[unique_id] = {}
        
        # Create a tuple for the period key
        period_key = (service_begin, service_end)

        # If the period exists, accumulate the usage
        if period_key in billing_data[unique_id]:
            billing_data[unique_id][period_key] += usage
        else:
            # Otherwise, initialize the usage for that period
            billing_data[unique_id][period_key] = usage

    return billing_data

def bill_count_per_unique_id_per_period(data):
    billing_data = {}

    for entry in data:
        unique_id = f"{entry['Location Name']}-{entry['Account #']}-{entry['Service Type']}"
        service_begin = parse_date(entry['Service Begin Date'])
        service_end = parse_date(entry['Service End Date'])
        bill_image = entry['Bill Image']

        # Initialize the dictionary for the unique_id if not already present
        if unique_id not in billing_data:
            billing_data[unique_id] = {}
        
        # Create a tuple for the period key
        period_key = (service_begin, service_end)

        # If the period exists, add the bill_image to the set
        if period_key in billing_data[unique_id]:
            billing_data[unique_id][period_key].add(bill_image)
        else:
            # Otherwise, initialize a set for that period and add the bill_image
            billing_data[unique_id][period_key] = {bill_image}

    # Convert the sets to their lengths (i.e., count of unique bill images)
    for unique_id, periods in billing_data.items():
        for period in periods:
            periods[period] = len(periods[period])

    return billing_data


def check_overlaps(data):
    billing_periods = {}
    duplicates = []
    overlaps = []

    for entry in data:
        unique_id = f"{entry['Location Name']}-{entry['Account #']}-{entry['Service Type']}"
        service_begin = parse_date(entry['Service Begin Date'])
        service_end = parse_date(entry['Service End Date'])
        bill_image = entry['Bill Image']

        if unique_id not in billing_periods:
            billing_periods[unique_id] = []
        
        # Check for duplicates and overlapping dates
        for (begin, end, bill) in billing_periods[unique_id]:
            if service_begin == begin and service_end == end and bill_image != bill:
                # Add the Unique ID to the entry
                entry['Unique ID'] = unique_id
                duplicates.append(entry)
            elif service_begin <= end and service_end >= begin:
                # Add the Unique ID to the entry
                entry['Unique ID'] = unique_id
                overlaps.append(entry)
        
        # Add the current billing period to the tracking list
        billing_periods[unique_id].append((service_begin, service_end, bill_image))
    
    return duplicates, overlaps



if __name__ == '__main__':
    folder_path = "/home/walmer/Projects/HighgateDashboard/.private/Engie Data/Data_InvoiceDetail"
    data = process_folder(folder_path)

    # duplicates, overlaps = check_overlaps(data)
    # pprint("Duplicates:")
    # for dup in duplicates:
    #     print(dup)

    # print("Overlaps:")
    # for overlap in overlaps:
    #     print(overlap)

    # # Output example
    # for unique_id, periods in billing_data.items():
    #     print(f"Unique ID: {unique_id}")
    #     for period, usage in periods.items():
    #         pprint(f"  Service Begin Date: {period[0]}, Service End Date: {period[1]}, Accumulated Usage: {usage}")

    billing_data = bill_count_per_unique_id_per_period(data)
    # Now you can iterate over the resulting dictionary
    for unique_id, periods in billing_data.items():
        for period, distinct_count in periods.items():
            if distinct_count > 1:
                print(f"Unique ID: {unique_id}")
                print(f"  Service Begin Date: {period[0]}, Service End Date: {period[1]}, Distinct Bill Images: {distinct_count}")
