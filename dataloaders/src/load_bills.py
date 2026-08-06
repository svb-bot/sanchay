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
from config import (
    DATE_FORMAT,
    ELECT_CATEGORY,
    RENT_CATEGORY,
    GAS_CATEGORY,
    GROCERY_CATEGORY,
    UPI_MODE,
    ACH_MODE,
    SI_MODE,
    FOOD_OFFICE_CATEGORY,
    MEDICINE_CATEGORY,
    OFFICE_BUS_CATEGORY,
    OFFICE_AUTO_CATEGORY,
)
from typing import List


def load_bnk_stmt_bills(
    file_path: str, categories: List[str], modes: List[str], load_main: bool = False
):
    """
    Load common UPI bills from a CSV file and process them.
    """
    # Implement the logic to read the CSV file and process the bills
    print(f"Loading rent bills from {file_path}")

    try:
        df = get_dataframe(file_path)
        txn_cols = derive_transaction_columns(df)
        print(txn_cols)

        with get_db_connection() as conn:
            with conn.cursor() as cursor:

                # owners_pattern = f"\\b(?:{'|'.join(RENT_OWNERS)})\\b"
                cursor.execute(
                    """select GROUP_CONCAT(pattern_name SEPARATOR '|') from dim_txn_pattern 
                        where category_name in ({categories_str})""".format(
                        categories_str=",".join(
                            [f"'{category}'" for category in categories]
                        )
                    )
                )
                owners_pattern = f"\\b(?:{str(cursor.fetchone()[0])})\\b"

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

                df["bill_issuer_name"] = (
                    df[txn_cols.get("details_column_name", "Narration")]
                    .str.split("-")
                    .str[1]
                )

                category_issuer_df = pd.read_sql_query(
                    """select pattern_name bill_issuer_name, category_name bill_category from dim_txn_pattern where category_name in ({categories_str})""".format(
                        categories_str=",".join(
                            [f"'{category}'" for category in categories]
                        )
                    ),
                    con=conn,
                )

                df = df.merge(
                    category_issuer_df,
                    how="left",
                    left_on="bill_issuer_name",
                    right_on="bill_issuer_name",
                )

                # Fetch the bill_payment_mode_id for 'UPI' from the database
                bill_payment_mode_df = pd.read_sql_query(
                    "select mode_id bill_payment_mode_id, mode_name bill_payment_mode from dim_bill_payment_mode where mode_name in ({modes_str})".format(
                        modes_str=",".join([f"'{mode}'" for mode in modes])
                    ),
                    con=conn,
                )

                # Fetch the payment_category_id for 'Rent' from the database
                bill_category_df = pd.read_sql_query(
                    """select category_id bill_category_id, category_name bill_category from dim_bill_category where category_name in ({categories_str})""".format(
                        categories_str=",".join(
                            [f"'{category}'" for category in categories]
                        )
                    ),
                    con=conn,
                )

                df["bill_payment_mode"] = (
                    df[txn_cols.get("details_column_name", "Narration")]
                    .str.split("-")
                    .str[0]
                )
                # df["bill_category"] = category
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
                df["upi_id"] = df[
                    txn_cols.get("details_column_name", "Narration")
                ].str.extract(r"([A-Za-z0-9._]{6,}@[A-Za-z0-9._]+)", expand=False)

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
                df["bill_amount"] = df.apply(
                    lambda row: (
                        float(row[txn_cols.get("deposit_column_name", "Deposit")]) * -1
                        if str(row["bill_amount"]) == "-"
                        else float(row["bill_amount"])
                    ),
                    axis=1,
                )

                df["bill_notes"] = df.apply(
                    lambda row: generate_notes(row, {"upi_id": "upi_id"}), axis=1
                )
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
        if load_main:
            load_into_main("fact_spending_stg", "fact_spending", ["bill_id"])

        print(f"{categories[0]} bills loaded successfully!")

    except Exception as e:
        print(f"Error loading {categories[0]} bills: {e}")
        raise


def load_cesc_bills(file_path):
    """
    Load CESC bills from a CSV file and process them.
    """
    # Implement the logic to read the CSV file and process the bills
    print(f"Loading CESC bills from {file_path}")

    try:
        df = get_dataframe(file_path)
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                # Check if the required columns are present in the DataFrame
                txn_cols = derive_transaction_columns(df)

                # Fetch the bill_payment_mode_id for 'SI' from the database
                bill_payment_mode_df = pd.read_sql_query(
                    f"select mode_id bill_payment_mode_id, mode_name bill_payment_mode from dim_bill_payment_mode where mode_name in ('{SI_MODE}', '{UPI_MODE}')",
                    con=conn,
                )

                # Fetch the bill_category_id for 'Electricity' from the database
                bill_category_df = pd.read_sql_query(
                    f"select category_id bill_category_id, category_name bill_category from dim_bill_category where category_name = '{ELECT_CATEGORY}'",
                    con=conn,
                )

                df["bill_payment_mode"] = df[
                    txn_cols.get("ref_column_name", "Cheque/Ref No")
                ].apply(lambda x: UPI_MODE if pd.isna(x) or pd.isnull(x) else SI_MODE)
                df[txn_cols.get("ref_column_name", "Cheque/Ref No")] = df[
                    txn_cols.get("ref_column_name", "Cheque/Ref No")
                ].apply(lambda x: None if pd.isna(x) or pd.isnull(x) else x)
                df["bill_category"] = ELECT_CATEGORY
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

                df[txn_cols.get("date_column_name", "Date")] = pd.to_datetime(
                    df[txn_cols.get("date_column_name", "Date")], format=DATE_FORMAT
                )
                df.rename(
                    columns={
                        txn_cols.get("date_column_name", "Date"): "bill_date",
                        txn_cols.get(
                            "issuer_column_name", "Issuer"
                        ): "bill_issuer_name",
                        txn_cols.get(
                            "withdrawal_column_name", "Withdrawal"
                        ): "bill_amount",
                        txn_cols.get(
                            "ref_column_name", "Cheque/Ref No"
                        ): "bill_reference",
                    },
                    inplace=True,
                )
                df["bill_notes"] = df.apply(
                    lambda row: generate_notes(
                        row,
                        {
                            "id": "txn_id",
                            txn_cols.get(
                                "consumer_column_name", "Consumer ID"
                            ): "consumer_id",
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
                print(df.head())

                # Process the data and insert into the database
            load_into_stg("fact_spending_stg", df)
            load_into_main("fact_spending_stg", "fact_spending", ["bill_id"])

            print("CESC bills loaded successfully!")

    except Exception as e:
        print(f"Error loading CESC bills: {e}")
        raise


def load_hpgas_bills(file_path):
    """
    Load HPGAS bills from a CSV file and process them.
    """
    # Implement the logic to read the CSV file and process the bills
    print(f"Loading HPGAS bills from {file_path}")

    try:
        df = get_dataframe(file_path)
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                # Check if the required columns are present in the DataFrame
                txn_cols = derive_transaction_columns(df)

                df[txn_cols.get("date_column_name", "Date")] = pd.to_datetime(
                    df[txn_cols.get("date_column_name", "Date")], dayfirst=True
                )
                df["bill_issuer_name"] = (
                    "Hindustan Petroleum Corporation Limited (HPCL)"
                )
                df["bill_category"] = GAS_CATEGORY
                df["bill_payment_mode"] = UPI_MODE
                category_df = pd.read_sql_query(
                    f"select category_id bill_category_id, category_name bill_category from dim_bill_category where category_name in ('{GAS_CATEGORY}')",
                    con=conn,
                )
                payment_mode_df = pd.read_sql_query(
                    f"select mode_id bill_payment_mode_id, mode_name bill_payment_mode from dim_bill_payment_mode where mode_name in ('{UPI_MODE}')",
                    con=conn,
                )
                print(payment_mode_df.head())
                df = df.merge(
                    category_df,
                    how="left",
                    left_on="bill_category",
                    right_on="bill_category",
                )
                df = df.merge(
                    payment_mode_df,
                    how="left",
                    left_on="bill_payment_mode",
                    right_on="bill_payment_mode",
                )

                df.rename(
                    columns={
                        txn_cols.get("date_column_name", "Date"): "bill_date",
                        "Amount": "bill_amount",
                        "HPGas Transaction No.": "bill_reference",
                    },
                    inplace=True,
                )
                df["bill_notes"] = df.apply(
                    lambda row: generate_notes(
                        row,
                        {
                            "PG Trans. No.": "txn_id",
                            "Booking Source": "src",
                            "Refill Order No.": "order_id",
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
                print(df.head())

            # Process the data and insert into the database
            load_into_stg("fact_spending_stg", df)
            load_into_main("fact_spending_stg", "fact_spending", ["bill_id"])

            print("HPGAS bills loaded successfully!")

    except Exception as e:
        print(f"Error loading HPGAS bills: {e}")
        raise


if __name__ == "__main__":
    load_dotenv()  # Load environment variables from .env file
    check_db()

    possible_types = [
        "cesc",
        "rent",
        "grocery",
        "medicine",
        "dining",
        "hpgas",
        "travel",
    ]
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
        load_bnk_stmt_bills(file_path, [RENT_CATEGORY], [UPI_MODE])
    elif bill_type == "grocery":
        load_bnk_stmt_bills(file_path, [GROCERY_CATEGORY], [UPI_MODE])
    elif bill_type == "dining":
        load_bnk_stmt_bills(file_path, [FOOD_OFFICE_CATEGORY], [UPI_MODE])
    elif bill_type == "medicine":
        load_bnk_stmt_bills(file_path, [MEDICINE_CATEGORY], [UPI_MODE], True)
    elif bill_type == "travel":
        load_bnk_stmt_bills(
            file_path, [OFFICE_BUS_CATEGORY, OFFICE_AUTO_CATEGORY], [UPI_MODE], True
        )
    elif bill_type == "hpgas":
        load_hpgas_bills(file_path)
