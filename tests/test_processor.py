from src.processor import process_csv

def test_process_csv():

    csv_data = """
customer_id,name,email
1,John,j@test.com
2,Mary,m@test.com
"""

    count = process_csv(csv_data)

    assert count == 2
