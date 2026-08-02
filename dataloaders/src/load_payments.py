from argparse import ArgumentParser
from dotenv import load_dotenv
from utils import get_db_connection, check_db, generate_notes
import pandas as pd

banking_map = {"HDFC": "HDFC Bank Limited"}


def load_interest_payments(file_path, bank_name="HDFC"):
    """
    Load interest payments from a CSV file and process them.
    """
    print(f"Loading interest payments from {file_path}")
    df = pd.read_csv(file_path)
    df = df[df["Narration"].str.lower().str.contains("interest", na=False)]

    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                required_columns = [
                    "Date",
                    "Narration",
                    "Chq./Ref.No.",
                    "Withdrawal Amt.",
                    "Deposit Amt.",
                ]
                missing_columns = [
                    col for col in required_columns if col not in df.columns
                ]
                if missing_columns:
                    raise ValueError(
                        f"Missing required columns in CSV: {', '.join(missing_columns)}"
                    )

                # Fetch the payment_mode_id for 'ECS' from the database
                payment_mode_df = pd.read_sql_query(
                    "select mode_id payment_mode_id, mode_name payment_mode from dim_payment_mode where mode_name = 'ECS'",
                    con=conn,
                )

                # Fetch the payment_category_id for Savings / FD from the database
                payment_category_df = pd.read_sql_query(
                    "select category_id payment_category_id, category_name payment_category from dim_payment_category where category_name in ('Interest/Savings', 'Interest/Deposit/Term')",
                    con=conn,
                )

                df["payment_mode"] = "ECS"
                df["payment_category"] = df["Narration"].apply(
                    lambda x: (
                        "Interest/Deposit/Term"
                        if "quarterly" in str(x).lower()
                        else "Interest/Savings"
                    )
                )
                df = df.merge(
                    payment_mode_df,
                    how="left",
                    left_on="payment_mode",
                    right_on="payment_mode",
                )
                df = df.merge(
                    payment_category_df,
                    how="left",
                    left_on="payment_category",
                    right_on="payment_category",
                )

                df["payment_payee_name"] = banking_map.get(bank_name, bank_name)
                df["Date"] = pd.to_datetime(df["Date"], format="mixed")
                df["acct_no"] = df["Narration"].str.extract(
                    r"QUARTERLY INTEREST CREDIT\s+(\d+)", expand=False
                )
                df.rename(
                    columns={
                        "Date": "payment_date",
                        "Deposit Amt.": "payment_amt",
                    },
                    inplace=True,
                )
                df["payment_notes"] = df.apply(
                    lambda row: generate_notes(
                        row,
                        {
                            "Chq./Ref.No.": "ref",
                            "acct_no": "acct_no",
                        },
                    ),
                    axis=1,
                )
                df.sort_values(by=["payment_category_id", "payment_date"], inplace=True)
                df = df[
                    [
                        "payment_date",
                        "payment_category_id",
                        "payment_payee_name",
                        "payment_amt",
                        "payment_mode_id",
                        "payment_notes",
                    ]
                ]
                df.reset_index(drop=True, inplace=True)
                print(df.head())

                cursor.executemany(
                    """
                    INSERT INTO fact_income (
                        payment_date,payment_category_id,payment_payee_name,payment_amt,payment_mode_id,payment_notes
                    ) VALUES (%s, %s, %s, %s, %s, %s)
                """,
                    (df.values.tolist()),
                )

                conn.commit()

    except Exception as e:
        print(f"Error loading interest payments: {e}")
        raise


def load_salary_payments(file_path):
    """
    Load salary payments from a CSV file and process them.
    """
    print(f"Loading salary payments from {file_path}")
    df = pd.read_csv(file_path)
    df = df[df["Narration"].str.lower().str.contains("salary", na=False)]

    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                required_columns = [
                    "Date",
                    "Narration",
                    "Chq./Ref.No.",
                    "Withdrawal Amt.",
                    "Deposit Amt.",
                ]
                missing_columns = [
                    col for col in required_columns if col not in df.columns
                ]
                if missing_columns:
                    raise ValueError(
                        f"Missing required columns in CSV: {', '.join(missing_columns)}"
                    )

                # Fetch the payment_mode_id for 'ACH'/'NEFT' from the database
                payment_mode_df = pd.read_sql_query(
                    "select mode_id payment_mode_id, mode_name payment_mode from dim_payment_mode where mode_name in ('ACH', 'NEFT')",
                    con=conn,
                )

                # Fetch the payment_category_id for Salary from the database
                payment_category_df = pd.read_sql_query(
                    "select category_id payment_category_id, category_name payment_category from dim_payment_category where category_name = 'Salary'",
                    con=conn,
                )

                df["payment_mode"] = df["Narration"].str.split().str[0]
                df["payment_category"] = "Salary"
                df = df.merge(
                    payment_mode_df,
                    how="left",
                    left_on="payment_mode",
                    right_on="payment_mode",
                )
                df = df.merge(
                    payment_category_df,
                    how="left",
                    left_on="payment_category",
                    right_on="payment_category",
                )

                df["payment_payee_name"] = df["Narration"].str.split("-").str[2]
                df["Date"] = pd.to_datetime(df["Date"], format="mixed")
                df.rename(
                    columns={
                        "Date": "payment_date",
                        "Deposit Amt.": "payment_amt",
                    },
                    inplace=True,
                )
                df["payment_notes"] = df.apply(
                    lambda row: generate_notes(
                        row,
                        {"Chq./Ref.No.": "ref"},
                    ),
                    axis=1,
                )
                df = df[
                    [
                        "payment_date",
                        "payment_category_id",
                        "payment_payee_name",
                        "payment_amt",
                        "payment_mode_id",
                        "payment_notes",
                    ]
                ]
                df.reset_index(drop=True, inplace=True)
                # print(df.tail())

                # Process the data and insert into the database
                cursor.executemany(
                    """
                    INSERT INTO fact_income (
                        payment_date,payment_category_id,payment_payee_name,payment_amt,payment_mode_id,payment_notes
                    ) VALUES (%s, %s, %s, %s, %s, %s)
                """,
                    (df.values.tolist()),
                )

                conn.commit()

    except Exception as e:
        print(f"Error loading salary payments: {e}")
        raise


if __name__ == "__main__":
    load_dotenv()  # Load environment variables from .env file
    check_db()

    possible_types = ["interest", "salary"]
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

    if bill_type == "interest":
        load_interest_payments(file_path)
    elif bill_type == "salary":
        load_salary_payments(file_path)
