import csv

def process_csv(file_content):

    reader = csv.DictReader(
        file_content.splitlines()
    )

    count = 0

    for row in reader:

        customer_id = row["customer_id"]

        print(
            f"Processing {customer_id}"
        )

        count += 1

    return count
