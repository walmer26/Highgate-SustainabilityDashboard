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
            "Supplier Only Account",
            "Audit Only",
            "Rate Schedule",
            "Month",
            "Service Days",
            "Cost",
            "Service Type",
            "UOM",
            "Usage",
            "KBTUs",
            "Open Exceptions",
            "Bundle",
            "Entity",
            "Total Bldg SqFt"
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
    folder_path = r"C:\Users\wramirez1\Downloads\Projects\Highgate-SustainabilityDashboard\.private\Engie Data\Data_UseCost"
    all_data = process_folder(folder_path)
    for x in all_data:
        print(x)
