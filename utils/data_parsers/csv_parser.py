import os
import csv


def parse_csv(file_path, delimiter=','):
    # Open the CSV file
    with open(file_path, mode='r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=delimiter)

        # Define the column names you want to extract
        column_names = [
            "Location Name",
            "Location #",
            "Vendor Name",
            "Account #",
            "Bill Month",
            "Bill Date",
            "Service Begin Date",
            "Service End Date",
            "Service Days",
            "Service Type",
            "UOM",
            "Usage",
            "Billed Quantity",
            "Cost",
            "Audit Only",
            "Entry Date",
            "Meter #",
            "Supplier Only Account",
            "Bill Image",
        ]

        # Ensure the CSV has the required columns
        if not set(column_names).issubset(reader.fieldnames):
            raise ValueError(f"CSV file at {file_path} does not contain required columns: {column_names}")

        # Iterate through the rows
        for row in reader:
            yield {name: row.get(name, '') for name in column_names}


def process_folder(folder_path):
    # Walk through the directory
    for dirpath, dirnames, files in os.walk(folder_path):
        for file_name in files:
            if file_name.endswith('.csv'):
                file_path = os.path.join(dirpath, file_name)
                yield from parse_csv(file_path)


if __name__ == "__main__":
    # Example usage
    folder_path = r"C:\Users\wramirez1\Downloads\Projects\Highgate-SustainabilityDashboard\.private\Engie Data\Data_InvoiceDetail"
    all_data = process_folder(folder_path)
    for x in all_data:
        print(x)
