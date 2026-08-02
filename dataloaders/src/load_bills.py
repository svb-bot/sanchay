from argparse import ArgumentParser
from dotenv import load_dotenv
from utils import get_db_connection, check_db, generate_notes
import pandas as pd


def load_cesc_bills(file_path):
    """
    Load CESC bills from a CSV file and process them.
    """
    # Implement the logic to read the CSV file and process the bills
    print(f"Loading CESC bills from {file_path}")
    # Example: Read the CSV and print the contents (replace with actual processing logic)

    df = pd.read_csv(file_path)
    # bill_date,bill_category_id,bill_issuer_name,bill_amount,bill_reference,bill_payment_mode_id,bill_notes
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                # Check if the required columns are present in the DataFrame
                required_columns = [
                    "date",
                    "issuer",
                    "amount",
                    "reference_no",
                    "id",
                    "consumer_id",
                ]
                missing_columns = [
                    col for col in required_columns if col not in df.columns
                ]
                if missing_columns:
                    raise ValueError(
                        f"Missing required columns in CSV: {', '.join(missing_columns)}"
                    )

                # Fetch the bill_payment_mode_id and bill_category_id from the database
                cursor.execute(
                    "select mode_id from dim_bill_payment_mode where mode_name = 'SI'"
                )
                bill_payment_mode_id = int(cursor.fetchone()[0] or 1)
                # Fetch the bill_category_id for 'Electricity' from the database
                cursor.execute(
                    "select category_id from dim_bill_category where category_name = 'Electricity'"
                )
                bill_category_id = int(cursor.fetchone()[0] or 1)
                df["bill_payment_mode_id"] = bill_payment_mode_id
                df["bill_category_id"] = bill_category_id
                df["date"] = pd.to_datetime(df["date"], format="%d-%b-%Y")
                df.rename(
                    columns={
                        "date": "bill_date",
                        "issuer": "bill_issuer_name",
                        "amount": "bill_amount",
                        "reference_no": "bill_reference",
                    },
                    inplace=True,
                )
                df["bill_notes"] = df.apply(
                    lambda row: generate_notes(
                        row,
                        {
                            "id": "txn_id",
                            "consumer_id": "consumer_id",
                        },
                    ),
                    axis=1,
                )
                df.drop(columns=["id", "consumer_id"], inplace=True)
                print(df.head())

                # Process the data and insert into the database
                cursor.executemany(
                    """
                    INSERT INTO fact_spending (
                        bill_date,
                        bill_category_id,
                        bill_issuer_name,
                        bill_amount,
                        bill_payment_mode_id,
                        bill_reference,
                        bill_notes
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """,
                    df[
                        [
                            "bill_date",
                            "bill_category_id",
                            "bill_issuer_name",
                            "bill_amount",
                            "bill_payment_mode_id",
                            "bill_reference",
                            "bill_notes",
                        ]
                    ].values.tolist(),
                )

                conn.commit()

    except Exception as e:
        print(f"Error loading CESC bills: {e}")
        return


if __name__ == "__main__":
    load_dotenv()  # Load environment variables from .env file
    check_db()

    possible_types = ["cesc"]
    parser = ArgumentParser()
    parser.add_argument(
        "--path",
        type=str,
        required=True,
        help="Path to the CSV file containing bills data",
    )
    parser.add_argument(
        "--type",
        type=str,
        required=True,
        choices=possible_types,
        help=f"Type of bills to loaded: {', '.join(possible_types)}",
    )
    args = parser.parse_args()

    file_path = args.path
    if args.type not in possible_types:
        raise ValueError(f"Invalid bill type. Must be {', '.join(possible_types)}.")
    bill_type = args.type

    if bill_type == "cesc":
        load_cesc_bills(file_path)
