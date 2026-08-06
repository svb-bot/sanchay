from argparse import ArgumentParser
from dotenv import load_dotenv
from utils import (
    get_db_connection,
    check_db,
    generate_notes,
    get_dataframe,
    load_into_stg,
    derive_transaction_columns,
    load_into_main,
)
import pandas as pd
import os
from config import (
    BANKING_MAP,
    DATE_FORMAT,
    ECS_MODE,
    UPI_MODE,
    ACH_MODE,
    NEFT_MODE,
    SAVINGS_CATEGORY,
    FD_CATEGORY,
    SALARY_CATEGORY
)


def load_interest_payments(file_path, bank_name="HDFC"):
    """
    Load interest payments from a CSV file and process them.
    """
    print(f"Loading interest payments from {file_path}")

    try:
        df = get_dataframe(file_path)
        txn_cols = derive_transaction_columns(df)
        print(txn_cols)

        df = df[
            df[txn_cols.get("details_column_name", "Narration")]
            .str.lower()
            .str.contains("interest", na=False)
        ]

        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                # Fetch the payment_mode_id for 'ECS' from the database
                payment_mode_df = pd.read_sql_query(
                    f"select mode_id payment_mode_id, mode_name payment_mode from dim_payment_mode where mode_name = '{ECS_MODE}'",
                    con=conn,
                )

                # Fetch the payment_category_id for Savings / FD from the database
                payment_category_df = pd.read_sql_query(
                    f"select category_id payment_category_id, category_name payment_category from dim_payment_category where category_name in ('{SAVINGS_CATEGORY}', '{FD_CATEGORY}')",
                    con=conn,
                )

                df["payment_mode"] = ECS_MODE
                df["payment_category"] = df[
                    txn_cols.get("details_column_name", "Narration")
                ].apply(
                    lambda x: (
                        FD_CATEGORY
                        if "quarterly" in str(x).lower()
                        else SAVINGS_CATEGORY
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

                df["payment_payee_name"] = BANKING_MAP.get(bank_name, bank_name)
                df[txn_cols.get("date_column_name", "Date")] = pd.to_datetime(
                    df[txn_cols.get("date_column_name", "Date")], format=DATE_FORMAT
                )
                df["acct_no"] = df[
                    txn_cols.get("details_column_name", "Narration")
                ].str.extract(r"QUARTERLY INTEREST CREDIT\s+(\d+)", expand=False)
                df.rename(
                    columns={
                        txn_cols.get("date_column_name", "Date"): "payment_date",
                        txn_cols.get(
                            "deposit_column_name", "Deposit Amt."
                        ): "payment_amt",
                    },
                    inplace=True,
                )
                df["payment_amt"] = (
                    df["payment_amt"].str.replace("-", "0").astype(float)
                )
                df["payment_notes"] = df.apply(
                    lambda row: generate_notes(
                        row,
                        {
                            txn_cols.get("ref_column_name", "Cheque/Ref No"): "ref",
                            "acct_no": "acct_no",
                        },
                    ),
                    axis=1,
                )
                # df.sort_values(by=["payment_category_id", "payment_date"], inplace=True)
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

        load_into_stg("fact_income_stg", df)
        load_into_main("fact_income_stg", "fact_income", ["payment_id"])

        print("Interest payments loaded successfully!")

    except Exception as e:
        print(f"Error loading interest payments: {e}")
        raise


def load_salary_payments(file_path):
    """
    Load salary payments from a CSV file and process them.
    """
    print(f"Loading salary payments from {file_path}")

    try:
        df = get_dataframe(file_path)
        txn_cols = derive_transaction_columns(df)
        print(txn_cols)

        df = df[
            df[txn_cols.get("details_column_name", "Narration")]
            .str.lower()
            .str.contains("salary", na=False)
        ]

        with get_db_connection() as conn:
            with conn.cursor() as cursor:

                # Fetch the payment_mode_id for 'ACH'/'NEFT' from the database
                payment_mode_df = pd.read_sql_query(
                    "select mode_id payment_mode_id, mode_name payment_mode from dim_payment_mode where mode_name in ('{ACH_MODE}', '{NEFT_MODE}')".format(
                        ACH_MODE=ACH_MODE, NEFT_MODE=NEFT_MODE
                    ),
                    con=conn,
                )

                # Fetch the payment_category_id for Salary from the database
                payment_category_df = pd.read_sql_query(
                    "select category_id payment_category_id, category_name payment_category from dim_payment_category where category_name = '{SALARY_CATEGORY}'".format(
                        SALARY_CATEGORY=SALARY_CATEGORY
                    ),
                    con=conn,
                )

                df["payment_mode"] = (
                    df[txn_cols.get("details_column_name", "Narration")]
                    .str.split()
                    .str[0]
                )
                df["payment_category"] = SALARY_CATEGORY
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

                df["payment_payee_name"] = (
                    df[txn_cols.get("details_column_name", "Narration")]
                    .str.split("-")
                    .str[2]
                )
                df[txn_cols.get("date_column_name", "Date")] = pd.to_datetime(
                    df[txn_cols.get("date_column_name", "Date")], format=DATE_FORMAT
                )
                df.rename(
                    columns={
                        txn_cols.get("date_column_name", "Date"): "payment_date",
                        txn_cols.get(
                            "deposit_column_name", "Deposit Amt."
                        ): "payment_amt",
                    },
                    inplace=True,
                )
                df["payment_amt"] = (
                    df["payment_amt"].str.replace("-", "0").astype(float)
                )
                df["payment_notes"] = df.apply(
                    lambda row: generate_notes(
                        row,
                        {txn_cols.get("ref_column_name", "Cheque/Ref No"): "ref"},
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
                print(df.head())

        load_into_stg("fact_income_stg", df)
        load_into_main("fact_income_stg", "fact_income", ["payment_id"])

        print("Salary payments loaded successfully!")

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
