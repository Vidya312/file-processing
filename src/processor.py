import csv

def process_csv(file_content):

    lines = [
        line.strip()
        for line in file_content.splitlines()
        if line.strip()
    ]

    reader = csv.DictReader(lines)

    count = 0

    for row in reader:

        customer_id = row.get("customer_id")

        if not customer_id:
            continue

        print(
            f"Processing {customer_id}"
        )

        count += 1

    return count
