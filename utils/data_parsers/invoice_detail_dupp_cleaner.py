import csv
from datetime import datetime
from decimal import Decimal
from invoice_detail_csv_parser import process_folder


def parse_date(date_str):
    """Helper function to parse date strings into datetime objects."""
    return datetime.strptime(date_str, '%m/%d/%Y')


def summary_per_unique_key(data):
    """
    It returns a dictionary with a unique_key as a combination of 'Location name', 'Account #' and 'Service Type'.
    Each unique_key combination key has sub-dictionaries with a tuple as period_key and another sub-dictionary as value < period_key:{} >.
    In the last dictionary (which is the value part of the 'period_key') we are having key:value pairs, which keys are the titles
    of the Set() we are having as its values for each case with its Usage Total in Decimal type. See a visual schema below:   

        billing_data = {
            unique_id:{
                period_key:{
                    "Bill Images Count":set(),
                    "Entry Dates Count":set(),
                    "Total Usage": 0,
                },
                period_key:{
                    "Bill Images Count":set(),
                    "Entry Dates Count":set(),
                    "Total Usage": 0,
                },
            },
            unique_id:{
                period_key:{
                    "Bill Images Count":set(),
                    "Entry Dates Count":set(),
                    "Total Usage": 0,
                },
                period_key:{
                    "Bill Images Count":set(),
                    "Entry Dates Count":set(),
                    "Total Usage": 0,
                },
            },
        }

    """

    billing_data = {}

    # starting the iteration of the generator
    for entry in data:
        # Declaring variables on iterating line that will be used
        unique_id = f"{entry['Location Name']}-{entry['Account #']}-{entry['Service Type']}"
        service_begin = parse_date(entry['Service Begin Date'])
        service_end = parse_date(entry['Service End Date'])
        bill_image = entry['Bill Image']
        entry_date = parse_date(entry["Entry Date"])
        usage = Decimal(entry['Usage'])
        unit = entry["UOM"].lower()

        # These are statistical units to avoid record usage on them
        avoid_stats_units = ["kw", "kvar", "kvarh", "kva"]

        # Initialize the dictionary for the unique_id if not already present
        if unique_id not in billing_data:
            billing_data[unique_id] = {}

        # Create a tuple for the period key
        period_key = (service_begin, service_end)
        # Initialize the dictionary for the period_key if not already present
        if period_key not in billing_data[unique_id]:
            billing_data[unique_id][period_key] = {
                "Bill Images Set": set(),
                "Entry Dates Set": set(),
                "Total Usage": 0,
            }

        # Add the current bill image and entry date to the sets
        if unit not in avoid_stats_units and usage != 0:
            billing_data[unique_id][period_key]["Total Usage"] += usage
            billing_data[unique_id][period_key]["Bill Images Set"].add(bill_image)
            billing_data[unique_id][period_key]["Entry Dates Set"].add(entry_date)

    # Convert the sets to their counts instead
    for unique_id, periods in billing_data.items():
        for period_key in periods:
            periods[period_key]["Bill Images Count"] = len(periods[period_key].pop("Bill Images Set"))
            periods[period_key]["Entry Dates Count"] = len(periods[period_key].pop("Entry Dates Set"))

    return billing_data


def export_dupp_summary_per_unique_key_to_csv(billing_data, filename):
    """Exports Engie Data considered duplicated to a CSV file."""
    
    header = ['Unique ID', 'Service Begin Date', 'Service End Date', 'Bill Images Count', 'Entry Dates Count', 'Total Usage']
    
    with open(filename, mode='w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(header)
        
        for unique_id, periods in billing_data.items():
            for period_key, counts in periods.items():
                bill_count = counts["Bill Images Count"]
                entry_dates_count = counts["Entry Dates Count"]
                total_usage = counts["Total Usage"]
                service_begin, service_end = period_key
                if bill_count > 1 or entry_dates_count > 1:
                    if total_usage != 0:
                        writer.writerow([
                            unique_id, 
                            service_begin.strftime('%m/%d/%Y'), 
                            service_end.strftime('%m/%d/%Y'), 
                            bill_count, 
                            entry_dates_count,
                            total_usage
                        ])

    print(f"Billing data successfully exported to {filename}")



# Usage example
if __name__ == '__main__':
    folder_path = r"C:\Users\wramirez1\Downloads\Projects\Highgate-SustainabilityDashboard\.private\Engie Data\Data_InvoiceDetail"
    data = process_folder(folder_path)
    dupp_billing_data = summary_per_unique_key(data)
    export_dupp_summary_per_unique_key_to_csv(dupp_billing_data, './.private/billing_data.csv')