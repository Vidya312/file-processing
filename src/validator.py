import csv

REQUIRED_COLUMNS = [
    "customer_id",
    "name",
    "email"
]

def validate_csv(file_content):

    reader = csv.DictReader(
        file_content.splitlines()
    )

    columns = reader.fieldnames

    missing = [
        c for c in REQUIRED_COLUMNS
        if c not in columns
    ]

    if missing:
        raise Exception(
            f"Missing columns: {missing}"
        )

    return True
