from argparse import ArgumentParser
from dotenv import load_dotenv
from utils import (
    get_db_connection,
    check_db,
    generate_notes,
    get_dataframe,
    derive_transaction_columns,
    load_into_stg,
    load_into_main,
)
import pandas as pd
from config import DATE_FORMAT, RENT_OWNERS, RENT_CATEGORY


def load_rent_bills(file_path):
    """
    Load rent bills from a CSV file and process them.
    """
    # Implement the logic to read the CSV file and process the bills
    print(f"Loading rent bills from {file_path}")

    try:
        df = get_dataframe(file_path)
        txn_cols = derive_transaction_columns(df)
        print(txn_cols)

        owners_pattern = f"\\b(?:{'|'.join(RENT_OWNERS)})\\b"
        df = df[
            df[txn_cols.get("details_column_name", "Narration")]
            .str.lower()
            .str.contains(
                owners_pattern,
                case=False,
                na=False,
                regex=True,
            )
        ]

        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                # Fetch the bill_payment_mode_id for 'UPI' from the database
                bill_payment_mode_df = pd.read_sql_query(
                    "select mode_id bill_payment_mode_id, mode_name bill_payment_mode from dim_bill_payment_mode where mode_name in ('UPI')",
                    con=conn,
                )

                # Fetch the payment_category_id for 'Rent' from the database
                bill_category_df = pd.read_sql_query(
                    f"select category_id bill_category_id, category_name bill_category from dim_bill_category where category_name in ('{RENT_CATEGORY}')",
                    con=conn,
                )

                df["bill_payment_mode"] = (
                    df[txn_cols.get("details_column_name", "Narration")]
                    .str.split("-")
                    .str[0]
                )
                df["bill_category"] = RENT_CATEGORY
                df = df.merge(
                    bill_payment_mode_df,
                    how="left",
                    left_on="bill_payment_mode",
                    right_on="bill_payment_mode",
                )
                df = df.merge(
                    bill_category_df,
                    how="left",
                    left_on="bill_category",
                    right_on="bill_category",
                )

                df["bill_issuer_name"] = (
                    df[txn_cols.get("details_column_name", "Narration")]
                    .str.split("-")
                    .str[1]
                )
                df[txn_cols.get("date_column_name", "Date")] = pd.to_datetime(
                    df[txn_cols.get("date_column_name", "Date")], format=DATE_FORMAT
                )
                df.rename(
                    columns={
                        txn_cols.get("date_column_name", "Date"): "bill_date",
                        txn_cols.get(
                            "withdrawal_column_name", "Withdrawal"
                        ): "bill_amount",
                        txn_cols.get(
                            "ref_column_name", "Cheque/Ref No"
                        ): "bill_reference",
                    },
                    inplace=True,
                )
                df["bill_notes"] = None
                df = df[
                    [
                        "bill_date",
                        "bill_category_id",
                        "bill_issuer_name",
                        "bill_reference",
                        "bill_amount",
                        "bill_payment_mode_id",
                        "bill_notes",
                    ]
                ]
                df.reset_index(drop=True, inplace=True)
                print(df.head())

        load_into_stg("fact_spending_stg", df)
        load_into_main("fact_spending_stg", "fact_spending", ["bill_id"])

        print("Rent bills loaded successfully!")

    except Exception as e:
        print(f"Error loading rent bills: {e}")
        return


def load_cesc_bills(file_path):
    """
    Load CESC bills from a CSV file and process them.
    """
    # Implement the logic to read the CSV file and process the bills
    print(f"Loading CESC bills from {file_path}")

    df = get_dataframe(file_path)

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

                # Fetch the bill_payment_mode_id for 'SI' from the database
                bill_payment_mode_df = pd.read_sql_query(
                    "select mode_id bill_payment_mode_id, mode_name bill_payment_mode from dim_bill_payment_mode where mode_name in ('SI', 'UPI')",
                    con=conn,
                )

                # Fetch the bill_category_id for 'Electricity' from the database
                bill_category_df = pd.read_sql_query(
                    "select category_id bill_category_id, category_name bill_category from dim_bill_category where category_name = 'Housing & Utilities/Electricity'",
                    con=conn,
                )

                df["bill_payment_mode"] = df["reference_no"].apply(
                    lambda x: "UPI" if pd.isna(x) or pd.isnull(x) else "SI"
                )
                df["reference_no"] = df["reference_no"].apply(
                    lambda x: None if pd.isna(x) or pd.isnull(x) else x
                )
                df["bill_category"] = "Housing & Utilities/Electricity"
                df = df.merge(
                    bill_payment_mode_df,
                    how="left",
                    left_on="bill_payment_mode",
                    right_on="bill_payment_mode",
                )
                df = df.merge(
                    bill_category_df,
                    how="left",
                    left_on="bill_category",
                    right_on="bill_category",
                )

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
                df = df[
                    [
                        "bill_date",
                        "bill_category_id",
                        "bill_issuer_name",
                        "bill_amount",
                        "bill_payment_mode_id",
                        "bill_reference",
                        "bill_notes",
                    ]
                ]
                df.reset_index(drop=True, inplace=True)
                print(df.head(100))

                # Process the data and insert into the database
                cursor.executemany(
                    """
                    INSERT INTO fact_spending_stg (
                        bill_date,
                        bill_category_id,
                        bill_issuer_name,
                        bill_amount,
                        bill_payment_mode_id,
                        bill_reference,
                        bill_notes
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """,
                    df.values.tolist(),
                )

                conn.commit()

    except Exception as e:
        print(f"Error loading CESC bills: {e}")
        return


if __name__ == "__main__":
    load_dotenv()  # Load environment variables from .env file
    check_db()

    possible_types = ["cesc", "rent"]
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
    elif bill_type == "rent":
        load_rent_bills(file_path)
